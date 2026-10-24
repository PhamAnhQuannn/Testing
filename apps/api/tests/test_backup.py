import sqlite3
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.backup import select_keep
from app.main import create_app
from app.models import tables as t
from app.runtime import Runtime


def names(client):
    return [b["name"] for b in client.get("/api/backups").json()["backups"]]


def put_draft(client, code):
    return client.put(
        "/api/drafts/add-two",
        json={"code": code, "updated_at": client.app.state.rt.clock().isoformat()},
    )


def draft_code(client):
    return client.get("/api/drafts/add-two").json()["draft"]["code"]


def test_create_list_download(client, clock):
    assert names(client) == []  # a brand-new DB is not backed up at start
    r = client.post("/api/backups")
    assert r.status_code == 201
    assert r.json()["name"] == "app-20261102-030000.db"
    clock.advance(seconds=1)
    client.post("/api/backups")
    assert names(client) == ["app-20261102-030001.db", "app-20261102-030000.db"]  # newest first
    client.post("/api/backups")  # same second as nothing advanced: unique name
    clock.advance(seconds=0)
    got = client.get("/api/backups/app-20261102-030000.db")
    assert got.status_code == 200 and got.content[:15] == b"SQLite format 3"
    assert client.get("/api/backups/../../etc/passwd").status_code in (404, 400)
    assert client.get("/api/backups/evil.db").json()["error"]["code"] == "invalid_backup_name"
    assert client.get("/api/backups/app-20200101-000000.db").json()["error"]["code"] == (
        "backup_not_found"
    )


def test_backup_is_a_consistent_copy(client, settings):
    put_draft(client, "hello")
    info = client.post("/api/backups").json()
    con = sqlite3.connect(settings.backups_path / info["name"])
    assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert con.execute("SELECT code FROM drafts").fetchone() == ("hello",)
    con.close()


def test_retention_20_recent_plus_first_of_each_day_for_30_days():
    now = datetime(2026, 11, 30, 12, tzinfo=UTC)

    def n(dt):
        return f"app-{dt:%Y%m%d-%H%M%S}.db"

    day10 = [datetime(2026, 11, 10, h, tzinfo=UTC) for h in (1, 7, 13, 19)]  # 4 on one day
    day11 = [datetime(2026, 11, 11, h, tzinfo=UTC) for h in (1, 7)]
    old = [datetime(2026, 9, 1, 5, tzinfo=UTC)]  # older than 30 days
    recent = [datetime(2026, 11, 30, 0, 0, i, tzinfo=UTC) for i in range(20)]
    all_names = [n(d) for d in day10 + day11 + old + recent]
    keep = select_keep(all_names, now)
    assert {n(d) for d in recent} <= keep
    assert n(day10[0]) in keep and n(day11[0]) in keep  # first of the day
    assert n(day10[1]) not in keep and n(day10[3]) not in keep and n(day11[1]) not in keep
    assert n(old[0]) not in keep
    assert select_keep(["junk.db", n(recent[0])], now) == {n(recent[0])}


def test_prune_runs_after_each_backup(client, clock, settings):
    client.app.state.rt.backups.keep_recent = 3
    for _ in range(6):
        client.post("/api/backups")
        clock.advance(minutes=1)
    # all in one day: 3 newest + the first of the day
    assert len(names(client)) == 4
    assert names(client)[-1] == "app-20261102-030000.db"


def test_restore_brings_back_the_old_data_and_snapshots_the_current(client, clock):
    put_draft(client, "before")
    saved = client.post("/api/backups").json()["name"]
    clock.advance(minutes=5)
    put_draft(client, "after")
    assert draft_code(client) == "after"
    r = client.post(f"/api/backups/{saved}/restore")
    assert r.status_code == 200 and r.json()["restored"]["name"] == saved
    assert draft_code(client) == "before"
    # the state being replaced was backed up first
    assert len(names(client)) == 2
    pre = [n for n in names(client) if n != saved][0]
    con = sqlite3.connect(client.app.state.rt.settings.backups_path / pre)
    assert con.execute("SELECT code FROM drafts").fetchone() == ("after",)
    con.close()
    # still durable and writable afterwards
    assert client.get("/api/health").json()["journal_mode"] == "wal"
    put_draft(client, "again")
    assert draft_code(client) == "again"


def test_restore_validation(client, settings):
    assert client.post("/api/backups/nope.db/restore").json()["error"]["code"] == (
        "invalid_backup_name"
    )
    assert client.post("/api/backups/app-20200101-000000.db/restore").status_code == 404
    settings.backups_path.mkdir(parents=True, exist_ok=True)
    (settings.backups_path / "app-20200101-000000.db").write_bytes(b"garbage" * 500)
    r = client.post("/api/backups/app-20200101-000000.db/restore")
    assert r.status_code == 422 and r.json()["error"]["code"] == "backup_corrupt"
    # a valid sqlite file from a newer/unknown schema is refused
    other = settings.backups_path / "app-20200102-000000.db"
    con = sqlite3.connect(other)
    con.execute("CREATE TABLE alembic_version (version_num VARCHAR(32))")
    con.execute("INSERT INTO alembic_version VALUES ('9999')")
    con.commit()
    con.close()
    r = client.post("/api/backups/app-20200102-000000.db/restore")
    assert r.status_code == 422 and r.json()["error"]["code"] == "schema_mismatch"
    assert client.get("/api/health").status_code == 200  # the live DB was left alone


def test_corrupt_db_then_restore_from_backup(settings, clock):
    rt = Runtime(settings, clock=clock)
    with TestClient(create_app(settings, rt)) as c:
        put_draft(c, "precious")
        name = c.post("/api/backups").json()["name"]
    # damage the live file (keeping the backup)
    settings.db_path.write_bytes(b"\x00corrupt" * 4096)
    rt2 = Runtime(settings, clock=clock)
    rt2.backup_on_shutdown = False
    with TestClient(create_app(settings, rt2)) as c:
        assert c.get("/api/health").status_code == 503
        assert (
            c.get("/api/health").json()["latest_backup"].startswith("app-20261102-030000")
        )  # shutdown copy: newest
        r = c.post(f"/api/backups/{name}/restore")
        assert r.status_code == 200
        assert c.get("/api/health").json()["status"] == "ok"
        assert draft_code(c) == "precious"
        assert c.get("/api/map").status_code == 200
    assert list(settings.data_dir.glob("app.db.corrupt-*"))  # the damaged file is kept aside


def test_backup_on_start_only_when_the_latest_is_older_than_1h(settings, clock):
    def run():
        rt = Runtime(settings, clock=clock)
        rt.backup_on_shutdown = False
        with TestClient(create_app(settings, rt)) as c:
            return names(c)

    assert run() == []  # first ever start: nothing to protect
    assert len(run()) == 1  # no backup yet -> take one
    clock.advance(minutes=59)
    assert len(run()) == 1
    clock.advance(minutes=2)
    assert len(run()) == 2


def test_scheduled_backup_every_6_hours(client, clock):
    rt = client.app.state.rt
    assert rt.scheduled_backup_tick() is not None  # none yet
    clock.advance(hours=5, minutes=59)
    assert rt.scheduled_backup_tick() is None
    clock.advance(minutes=2)
    assert rt.scheduled_backup_tick() is not None
    # the interval is a setting
    client.put("/api/settings", json={"backup_every_hours": 1})
    clock.advance(minutes=61)
    assert rt.scheduled_backup_tick() is not None
    assert len(names(client)) == 3


def test_backup_on_graceful_shutdown_and_mirror(settings, clock, tmp_path):
    settings.backup_mirror_dir = tmp_path / "cloud"
    rt = Runtime(settings, clock=clock)
    with TestClient(create_app(settings, rt)):
        pass
    assert len(list(settings.backups_path.glob("app-*.db"))) == 1
    assert len(list((tmp_path / "cloud").glob("app-*.db"))) == 1


def test_restore_keeps_progress_rows_consistent(client, clock):
    """After a restore the app serves the restored progress (events and caches together)."""
    client.post("/api/lessons/py.a.one/runs")
    saved = client.post("/api/backups").json()["name"]
    client.post("/api/lessons/py.a.one/runs")
    assert client.get("/api/lessons/py.a.one").json()["progress"]["run_no"] == 3
    clock.advance(minutes=1)
    client.post(f"/api/backups/{saved}/restore")
    assert client.get("/api/lessons/py.a.one").json()["progress"]["run_no"] == 2
    with client.app.state.rt.session() as db:
        assert len(db.scalars(select(t.Event).where(t.Event.type == "lesson_run")).all()) == 1


def test_restore_of_a_pruneable_backup_survives_the_pre_restore_snapshot(client, clock):
    put_draft(client, "v0")
    for i in range(21):  # 21 backups, 1 s apart, same day: 20 newest + the oldest are kept
        clock.advance(seconds=1)
        put_draft(client, f"v{i + 1}")
        client.post("/api/backups")
    listed = names(client)
    assert len(listed) == 21
    chosen = listed[-2]  # second oldest: the snapshot's prune would delete it
    r = client.post(f"/api/backups/{chosen}/restore")
    assert r.status_code == 200 and r.json()["restored"]["name"] == chosen
    assert client.get("/api/health").status_code == 200
    assert chosen in names(client)
    assert draft_code(client) == "v2"


def test_failed_restore_keeps_serving_the_old_data(client, clock, monkeypatch):
    put_draft(client, "keep me")
    name = client.post("/api/backups").json()["name"]
    clock.advance(minutes=1)
    put_draft(client, "newer")

    def boom(*_a, **_k):
        raise RuntimeError("disk gone")

    monkeypatch.setattr(client.app.state.rt.backups, "restore_into", boom)
    with pytest.raises(RuntimeError, match="disk gone"):
        client.post(f"/api/backups/{name}/restore")
    assert client.get("/api/health").status_code == 200
    assert draft_code(client) == "newer"
    put_draft(client, "writable")
    assert draft_code(client) == "writable"


def test_backup_list_orders_same_second_names_numerically(client, clock):
    for _ in range(11):  # same second: app-..-.db, -1 ... -10
        client.post("/api/backups")
    listed = names(client)
    assert (
        listed[0].endswith("-10.db")
        and listed[-1].endswith("0.db")
        and "-" not in listed[-1][-8:-3]
    )
