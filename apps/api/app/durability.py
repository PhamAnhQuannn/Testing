"""Startup safety checks (SPEC 6.7): refuse network filesystems, require journal_mode=wal."""

from __future__ import annotations

import re
from pathlib import Path

from .errors import StartupError

# nfs, cifs/smb, fuse, 9p, vboxsf (SPEC 6.7). Prefix match on the fstype column of /proc/mounts.
NETWORK_FS_PREFIXES = ("nfs", "cifs", "smb", "9p", "vboxsf", "fuse")


def _unescape(s: str) -> str:
    return re.sub(r"\\([0-7]{3})", lambda m: chr(int(m.group(1), 8)), s)


def parse_mounts(text: str) -> list[tuple[str, str]]:
    """[(mount_point, fstype)] from /proc/mounts text."""
    out = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            out.append((_unescape(parts[1]), parts[2]))
    return out


def fs_type_for(path: Path, mounts: list[tuple[str, str]]) -> str | None:
    """fstype of the longest mount point that is a prefix of `path`."""
    p = str(path.resolve())
    best: tuple[int, str] | None = None
    for mp, fstype in mounts:
        norm = mp.rstrip("/") or "/"
        inside = p == norm or norm == "/" or p.startswith(norm + "/")
        if inside and (best is None or len(norm) > best[0]):
            best = (len(norm), fstype)
    return best[1] if best else None


def is_network_fs(fstype: str | None) -> bool:
    return bool(fstype) and fstype.lower().startswith(NETWORK_FS_PREFIXES)


def check_data_dir(data_dir: Path, mounts_file: Path, allow_network_fs: bool = False) -> None:
    """Raise StartupError when `data_dir` lives on a network/FUSE filesystem."""
    if allow_network_fs or not mounts_file.exists():
        return
    mounts = parse_mounts(mounts_file.read_text(errors="replace"))
    fstype = fs_type_for(data_dir, mounts)
    if is_network_fs(fstype):
        raise StartupError(
            f"The data directory {data_dir} is on a {fstype!r} filesystem. SQLite durability "
            "(fsync, WAL shared memory) is not guaranteed on network, FUSE or shared-folder "
            "filesystems, so the app refuses to start. Use a local disk or a Docker named volume."
        )
