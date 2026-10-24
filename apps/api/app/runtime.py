"""Process-wide state: engine, content, backups, and the boot/restore sequence."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import secrets
import sqlite3
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, delete
from sqlalchemy.orm import Session

from . import durability
from .backup import BackupInfo, BackupManager, integrity_ok, schema_version
from .config import API_ROOT, Settings
from .db import make_engine, pragma
from .errors import ApiError, StartupError
from .models import tables as t
from .services import progress
from .services.content_loader import ContentStore

log = logging.getLogger("prep.runtime")


def alembic_config(engine: Engine | None = None) -> Config:
    cfg = Config(str(API_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(API_ROOT / "migrations"))
    if engine is not None:
        cfg.attributes["engine"] = engine
    return cfg


def head_revision() -> str:
    return ScriptDirectory.from_config(alembic_config()).get_current_head() or ""


def known_revisions() -> set[str]:
    return {r.revision for r in ScriptDirectory.from_config(alembic_config()).walk_revisions()}


def utcnow() -> datetime:
    return datetime.now(UTC)


@dataclass
class Runtime:
    settings: Settings
    clock: Callable[[], datetime] = utcnow
    engine: Engine | None = None
    content: ContentStore | None = None
    degraded: str | None = None  # e.g. "db_corrupt"
    submit_tokens: dict[str, tuple[str, datetime]] = field(default_factory=dict)
    lock: threading.RLock = field(default_factory=threading.RLock)
    backup_on_shutdown: bool = True
    _task: asyncio.Task | None = None

    def __post_init__(self) -> None:
        s = self.settings
        self.backups = BackupManager(
            s.db_path,
            s.backups_path,
            lambda: self.clock(),
            s.backup_mirror_dir,
            keep_recent=self._backup_keep,
        )

    def _backup_keep(self) -> int:
        if self.engine is None:
            return 20
        try:
            with self.session() as db:
                row = db.get(t.UserSettings, progress.USER_ID)
                return row.backup_keep if row and row.backup_keep else 20
        except Exception:
            return 20

    # ---- sessions ----

    def session(self) -> Session:
        if self.engine is None:
            raise ApiError(
                503,
                "db_corrupt",
                "The database is damaged; restore a backup (POST /api/backups/{name}/restore)",
            )
        return Session(self.engine, expire_on_commit=False)

    # ---- boot ----

    def start(self) -> None:
        s = self.settings
        s.data_dir.mkdir(parents=True, exist_ok=True)
        durability.check_data_dir(s.data_dir, s.mounts_file, s.allow_network_fs)
        self.content = ContentStore.load(s.content_dir, s.serve_drafts)
        self._open(backup_if_due=True)

    def _quick_check(self) -> bool:
        try:
            con = sqlite3.connect(self.settings.db_path, timeout=5)
            try:
                return con.execute("PRAGMA quick_check").fetchone()[0] == "ok"
            finally:
                con.close()
        except sqlite3.DatabaseError:
            return False

    def _open(self, *, backup_if_due: bool) -> None:
        s = self.settings
        existed = s.db_path.exists() and s.db_path.stat().st_size > 0
        self.degraded = None
        if existed and not self._quick_check():
            log.error("quick_check failed for %s; starting in degraded mode", s.db_path)
            self.degraded = "db_corrupt"
            self.engine = None
            return
        engine = make_engine(s.db_path)
        mode = pragma(engine, "journal_mode").lower()
        if mode != "wal":
            raise StartupError(f"SQLite journal_mode is {mode!r}, expected 'wal'")
        if existed:
            rev = schema_version(s.db_path)
            if rev != head_revision() and self.settings.backups_enabled:
                self.backups.create()  # before any migration
            elif (
                backup_if_due
                and s.backups_enabled
                and self.backups.due(s.backup_on_start_if_older_than_s / 3600)
            ):
                self.backups.create()
        command.upgrade(alembic_config(engine), "head")
        self.engine = engine
        assert self.content is not None
        now = self.clock()
        with self.session() as db:
            self.content.sync_db(db)
            progress.ensure_user_rows(db, self.content, now)
            progress.sync_unlocks(db, self.content, now)
            progress.recompute_all(db, self.content, now)  # caches follow events (and content)
            cutoff = now - timedelta(days=s.idempotency_ttl_days)
            db.execute(delete(t.IdempotencyKey).where(t.IdempotencyKey.created_at < cutoff))
            db.commit()

    # ---- shutdown ----

    def stop(self) -> None:
        if self.engine is not None:
            if self.backup_on_shutdown and self.settings.backups_enabled:
                with contextlib.suppress(Exception):
                    self.backups.create()
            self.engine.dispose()
            self.engine = None

    # ---- scheduled backups ----

    def backup_every_hours(self) -> int:
        if self.engine is None:
            return 6
        with self.session() as db:
            row = db.get(t.UserSettings, progress.USER_ID)
            return row.backup_every_hours if row else 6

    def scheduled_backup_tick(self) -> BackupInfo | None:
        if self.engine is None or not self.settings.backups_enabled:
            return None
        if self.backups.due(self.backup_every_hours()):
            return self.backups.create()
        return None

    async def _loop(self) -> None:
        while True:
            await asyncio.sleep(self.settings.backup_poll_s)
            try:
                await asyncio.to_thread(self.scheduled_backup_tick)
            except Exception:
                log.exception("scheduled backup failed")

    def start_scheduler(self) -> None:
        if self.settings.backups_enabled:
            self._task = asyncio.get_running_loop().create_task(self._loop())

    async def stop_scheduler(self) -> None:
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

    # ---- restore ----

    def restore(self, name: str) -> BackupInfo:
        """Replace the live DB by backup `name` (SPEC 6.7 / UI_SPEC 4.7).

        Order: validate the chosen file (integrity_check, schema_version), back up the current DB,
        load the chosen one with the backup API, then run the normal open sequence.
        """
        with self.lock:
            path = self.backups.path_for(name)
            if not integrity_ok(path):
                raise ApiError(422, "backup_corrupt", f"{name} failed integrity_check")
            rev = schema_version(path)
            if rev is None or rev not in known_revisions():
                raise ApiError(
                    422,
                    "schema_mismatch",
                    f"{name} has schema version {rev!r}, unknown to this build",
                )
            target = self.settings.db_path
            staged = target.with_name(target.name + ".restoring")
            staged.unlink(missing_ok=True)
            swapped = False
            try:
                if self.engine is not None and self.degraded is None:
                    # snapshot of what is being replaced; the chosen file must survive its prune
                    self.backups.create(protect={name})
                self.backups.restore_into(name, staged)  # the live DB is untouched until the swap
                if not integrity_ok(staged):
                    raise ApiError(422, "backup_corrupt", f"{name} failed integrity_check")
                old, self.engine = self.engine, None
                swapped = True
                if old is not None:
                    old.dispose()
                if target.exists() and not self._quick_check():
                    stamp = self.clock().strftime("%Y%m%d-%H%M%S")
                    target.rename(target.with_name(f"app.db.corrupt-{stamp}"))
                for suffix in ("-wal", "-shm"):  # leftovers of the DB being replaced
                    Path(str(target) + suffix).unlink(missing_ok=True)
                staged.replace(target)
                self._open(backup_if_due=False)
            except BaseException:
                staged.unlink(missing_ok=True)
                if swapped and self.engine is None:
                    # back to serving whatever DB is on disk (the old one unless the swap happened)
                    with contextlib.suppress(Exception):
                        self._open(backup_if_due=False)
                raise
            info = next((b for b in self.backups.list() if b.name == name), None)
            assert info is not None
            return info

    def new_submit_token(self, problem_id: str) -> tuple[str, datetime]:
        token = secrets.token_urlsafe(24)
        expires = self.clock() + timedelta(seconds=self.settings.submit_token_ttl_s)
        now = self.clock()
        self.submit_tokens = {k: v for k, v in self.submit_tokens.items() if v[1] > now}
        self.submit_tokens[token] = (problem_id, expires)
        return token, expires

    def check_submit_token(self, token: str | None, problem_id: str) -> None:
        if not token:
            raise ApiError(
                403, "submit_token_required", "Call POST /problems/{id}/start-submit first"
            )
        got = self.submit_tokens.get(token)
        if got is None or got[0] != problem_id or got[1] <= self.clock():
            raise ApiError(403, "submit_token_expired", "The submit token is invalid or expired")
