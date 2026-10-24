import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import db as dbmod
from app.durability import check_data_dir, fs_type_for, is_network_fs, parse_mounts
from app.errors import StartupError
from app.main import create_app
from app.runtime import Runtime

MOUNTS = r"""
overlay / overlay rw,relatime 0 0
/dev/vda /data ext4 rw 0 0
server:/export /mnt/nfs nfs4 rw 0 0
//srv/share /mnt/smb cifs rw 0 0
share /mnt/vbox vboxsf rw 0 0
host /mnt/p9 9p rw 0 0
gvfs /mnt/fuse fuse.sshfs rw 0 0
//srv/My\040Share /mnt/with\040space smb3 rw 0 0
"""


def test_parse_and_classify():
    mounts = parse_mounts(MOUNTS)
    cases = {
        "/home/x": "overlay",
        "/data/app": "ext4",
        "/mnt/nfs/deep/dir": "nfs4",
        "/mnt/smb": "cifs",
        "/mnt/vbox/x": "vboxsf",
        "/mnt/p9/x": "9p",
        "/mnt/fuse/x": "fuse.sshfs",
        "/mnt/with space/x": "smb3",
        "/mnt/nfsish": "overlay",  # prefix of a name is not a mount boundary
    }
    for path, want in cases.items():
        assert fs_type_for(Path(path), mounts) == want, path
    assert [
        is_network_fs(f) for f in ("ext4", "overlay", "nfs", "nfs4", "cifs", "smb3", "fuse")
    ] == [
        False,
        False,
        True,
        True,
        True,
        True,
        True,
    ]
    assert all(is_network_fs(f) for f in ("9p", "vboxsf", "fuse.sshfs", "fuseblk", "smbfs"))


def test_check_data_dir_refuses_network_fs(tmp_path):
    mounts = tmp_path / "mounts"
    mounts.write_text(f"/dev/vda / ext4 rw 0 0\nsrv:/x {tmp_path}/net nfs rw 0 0\n")
    check_data_dir(tmp_path / "local", mounts)  # fine
    with pytest.raises(StartupError, match="nfs"):
        check_data_dir(tmp_path / "net" / "data", mounts)
    check_data_dir(tmp_path / "net" / "data", mounts, allow_network_fs=True)  # test override
    check_data_dir(tmp_path / "net", tmp_path / "missing-mounts-file")  # no /proc/mounts: skip


def test_app_refuses_to_start_on_network_fs(settings, tmp_path):
    mounts = tmp_path / "mounts"
    mounts.write_text(f"/dev/vda / ext4 rw 0 0\n//srv/x {settings.data_dir} cifs rw 0 0\n")
    settings.mounts_file = mounts
    settings.allow_network_fs = False
    with pytest.raises(StartupError, match="cifs"), TestClient(create_app(settings)):
        pass
    assert not settings.db_path.exists()  # nothing was written
    settings.allow_network_fs = True
    with TestClient(create_app(settings)) as c:
        assert c.get("/api/health").status_code == 200


def test_app_refuses_when_journal_mode_is_not_wal(settings, monkeypatch):
    def fake(conn):
        conn.execute("PRAGMA journal_mode=DELETE")
        return "delete"

    monkeypatch.setattr(dbmod, "apply_pragmas", fake)
    with pytest.raises(StartupError, match="wal"), TestClient(create_app(settings)):
        pass


def test_pragmas_on_every_connection(client):
    engine = client.app.state.rt.engine
    with engine.connect() as c:
        row = lambda p: c.exec_driver_sql(f"PRAGMA {p}").scalar()  # noqa: E731
        assert row("journal_mode") == "wal"
        assert row("synchronous") == 2
        assert row("foreign_keys") == 1
        assert row("busy_timeout") == 5000


def test_committed_data_survives_a_hard_stop(settings, clock):
    """A 2xx means committed: reopen the file with a fresh process-like connection."""
    rt = Runtime(settings, clock=clock)
    rt.backup_on_shutdown = False
    with TestClient(create_app(settings, rt)) as c:
        c.put(
            "/api/drafts/add-two",
            json={"code": "typed", "updated_at": "2026-11-02T03:00:00Z"},
        )
        # do NOT shut down cleanly: read the file as another process would
        con = sqlite3.connect(settings.db_path)
        assert con.execute("SELECT code FROM drafts").fetchone() == ("typed",)
        con.close()


def test_quick_check_failure_starts_degraded(settings, clock):
    with TestClient(create_app(settings, Runtime(settings, clock=clock))):
        pass
    settings.db_path.write_bytes(b"this is not a database" * 100)
    for suffix in ("-wal", "-shm"):
        Path(str(settings.db_path) + suffix).unlink(missing_ok=True)
    rt = Runtime(settings, clock=clock)
    with TestClient(create_app(settings, rt)) as c:
        h = c.get("/api/health")
        assert h.status_code == 503 and h.json()["status"] == "db_corrupt"
        r = c.get("/api/map")
        assert r.status_code == 503 and r.json()["error"]["code"] == "db_corrupt"
        assert c.get("/api/backups").status_code == 200
