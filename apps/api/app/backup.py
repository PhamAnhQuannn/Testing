"""Automatic backups with the SQLite online backup API (SPEC 6.7 / UI_SPEC 4.7)."""

from __future__ import annotations

import re
import shutil
import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .errors import ApiError

NAME_RE = re.compile(r"^app-(\d{8})-(\d{6})(-\d+)?\.db$")


@dataclass(frozen=True)
class BackupInfo:
    name: str
    size: int
    created_at: datetime


def parse_name(name: str) -> datetime | None:
    m = NAME_RE.match(name)
    if not m:
        return None
    return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S").replace(tzinfo=UTC)


def select_keep(
    names: list[str], now: datetime, keep_recent: int = 20, keep_days: int = 30
) -> set[str]:
    """Newest `keep_recent` backups plus the first one of each of the last `keep_days` days."""
    dated = sorted(
        ((parse_name(n), n) for n in names if parse_name(n)), key=lambda x: (x[0], len(x[1]), x[1])
    )
    keep = {n for _, n in dated[::-1][:keep_recent]}
    cutoff = (now - timedelta(days=keep_days)).date()
    seen_days = set()
    for dt, n in dated:  # oldest first, so the first one of a day wins
        if dt.date() < cutoff or dt.date() in seen_days:
            continue
        seen_days.add(dt.date())
        keep.add(n)
    return keep


def integrity_ok(path: Path) -> bool:
    try:
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5)
        try:
            return con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        finally:
            con.close()
    except sqlite3.DatabaseError:
        return False


def schema_version(path: Path) -> str | None:
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5)
    try:
        try:
            row = con.execute("SELECT version_num FROM alembic_version").fetchone()
        except sqlite3.DatabaseError:
            return None
        return row[0] if row else None
    finally:
        con.close()


class BackupManager:
    def __init__(
        self,
        db_path: Path,
        backup_dir: Path,
        clock: Callable[[], datetime],
        mirror_dir: Path | None = None,
        keep_recent: int | Callable[[], int] = 20,
    ) -> None:
        self.db_path = db_path
        self.dir = backup_dir
        self.clock = clock
        self.mirror = mirror_dir
        self.keep_recent = keep_recent

    def list(self) -> list[BackupInfo]:
        if not self.dir.exists():
            return []
        out = []
        for p in self.dir.iterdir():
            dt = parse_name(p.name)
            if dt and p.is_file():
                out.append(BackupInfo(p.name, p.stat().st_size, dt))
        # name length breaks ties within one second: app-..-10.db is newer than app-..-2.db
        return sorted(out, key=lambda b: (b.created_at, len(b.name), b.name), reverse=True)

    def latest(self) -> BackupInfo | None:
        items = self.list()
        return items[0] if items else None

    def path_for(self, name: str) -> Path:
        if not NAME_RE.match(name):
            raise ApiError(400, "invalid_backup_name", "Invalid backup name")
        p = self.dir / name
        if not p.is_file():
            raise ApiError(404, "backup_not_found", f"No backup named {name}")
        return p

    def create(self, protect: set[str] | None = None) -> BackupInfo:
        """Copy the live DB with the online backup API (never a plain file copy)."""
        self.dir.mkdir(parents=True, exist_ok=True)
        stamp = self.clock().astimezone(UTC).strftime("%Y%m%d-%H%M%S")
        name = f"app-{stamp}.db"
        n = 1
        while (self.dir / name).exists():
            name = f"app-{stamp}-{n}.db"
            n += 1
        final = self.dir / name
        tmp = self.dir / f".{name}.tmp"
        src = sqlite3.connect(self.db_path, timeout=10)
        try:
            dst = sqlite3.connect(tmp)
            try:
                src.backup(dst)
            finally:
                dst.close()
        finally:
            src.close()
        # A plain journal-mode copy: backups are standalone files.
        con = sqlite3.connect(tmp)
        try:
            con.execute("PRAGMA journal_mode=DELETE")
        finally:
            con.close()
        tmp.replace(final)
        if self.mirror:
            try:
                self.mirror.mkdir(parents=True, exist_ok=True)
                shutil.copy2(final, self.mirror / name)
            except OSError:
                pass  # the mirror is best effort
        self.prune(protect)
        return BackupInfo(name, final.stat().st_size, parse_name(name) or self.clock())

    def prune(self, protect: set[str] | None = None) -> list[str]:
        names = [b.name for b in self.list()]
        recent = self.keep_recent() if callable(self.keep_recent) else self.keep_recent
        keep = select_keep(names, self.clock(), recent) | (protect or set())
        removed = []
        for n in names:
            if n not in keep:
                (self.dir / n).unlink(missing_ok=True)
                removed.append(n)
        return removed

    def due(self, every_hours: float) -> bool:
        latest = self.latest()
        return latest is None or self.clock() - latest.created_at >= timedelta(hours=every_hours)

    def restore_into(self, name: str, target: Path) -> None:
        """Load backup `name` into the DB file `target` with the backup API."""
        src_path = self.path_for(name)
        src = sqlite3.connect(f"file:{src_path}?mode=ro", uri=True)
        try:
            dst = sqlite3.connect(target, timeout=10)
            try:
                src.backup(dst)
            finally:
                dst.close()
        finally:
            src.close()
