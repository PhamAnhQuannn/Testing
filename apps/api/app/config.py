"""Runtime settings, read from the environment (all overridable in tests via Settings(...))."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

API_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = API_ROOT.parent.parent


def _flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    data_dir: Path = field(
        default_factory=lambda: Path(os.environ.get("DATA_DIR", REPO_ROOT / "data"))
    )
    content_dir: Path = field(
        default_factory=lambda: Path(os.environ.get("CONTENT_DIR", REPO_ROOT / "content"))
    )
    backup_dir: Path | None = field(
        default_factory=lambda: (
            Path(os.environ["BACKUP_DIR"]) if os.environ.get("BACKUP_DIR") else None
        )
    )
    backup_mirror_dir: Path | None = field(
        default_factory=lambda: (
            Path(os.environ["BACKUP_MIRROR_DIR"]) if os.environ.get("BACKUP_MIRROR_DIR") else None
        )
    )
    # Dev mode: also serve lessons/problems whose status is not `published`.
    serve_drafts: bool = field(default_factory=lambda: _flag("SERVE_DRAFTS", False))
    # Escape hatch for tests (and for people who really know): skip the network-filesystem check.
    allow_network_fs: bool = field(default_factory=lambda: _flag("ALLOW_NETWORK_FS", False))
    mounts_file: Path = Path("/proc/mounts")
    backups_enabled: bool = True
    backup_on_start_if_older_than_s: int = 3600
    backup_poll_s: int = 60
    submit_token_ttl_s: int = 15 * 60
    idempotency_ttl_days: int = 30
    idempotency_pending_stale_s: int = 30
    tz: str = "Asia/Ho_Chi_Minh"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "app.db"

    @property
    def backups_path(self) -> Path:
        return self.backup_dir or (self.data_dir / "backups")
