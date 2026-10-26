"""Unlock wiring (SPEC 5.3): one-way `unlocked_at`, lock_reasons, tested_out, map status.

Fixture graph (conftest): py.a.one (assumed prereq) -> py.a.two -> py.a.three (also needs
`cs.outside`, which has no content). `one` plays the role of `arrays`, `two` of `hash_tables`.
"""

from app.models import tables as t
from app.services import progress


def entry(client, sid):
    return next(s for s in client.get("/api/map").json()["subtopics"] if s["id"] == sid)


def row(client, sid):
    with client.app.state.rt.session() as db:
        return db.get(t.UserSubtopic, (1, sid))


def add_check(client, clock, sid, level, passed=True, clean=True):
    rt = client.app.state.rt
    with rt.session() as db:
        db.add(
            t.CheckResult(
                user_id=1,
                subtopic_id=sid,
                item_id=f"Q{level}",
                level=level,
                passed=passed,
                clean=clean,
                taken_at=clock(),
                item_type="write_code",
            )
        )
        progress.recompute_subtopic(db, rt.content, sid, clock())
        db.commit()


def drop_checks(client, clock, sid):
    rt = client.app.state.rt
    with rt.session() as db:
        db.query(t.CheckResult).delete()
        progress.recompute_subtopic(db, rt.content, sid, clock())
        db.commit()


def test_assumed_prerequisite_unlocks_root_and_status_is_unlocked(client):
    one = entry(client, "py.a.one")
    assert one["unlocked"] and one["status"] == "unlocked" and one["lock_reasons"] == []
    assert row(client, "py.a.one").unlocked_at is not None


def test_locked_item_reports_prerequisite_and_score(client):
    two = entry(client, "py.a.two")
    assert not two["unlocked"] and two["status"] == "locked"
    assert row(client, "py.a.two").unlocked_at is None
    assert two["lock_reasons"] == [
        {
            "prerequisite": "py.a.one",
            "score": 0,
            "need": 2,
            "name_vi": "Mục py.a.one",
        }
    ]


def test_missing_content_prerequisite_is_reported(client):
    three = entry(client, "py.a.three")
    by_pre = {r["prerequisite"]: r for r in three["lock_reasons"]}
    assert by_pre["py.a.two"]["score"] == 0
    assert by_pre["cs.outside"]["missing_content"] is True
    assert three["status"] == "blocked_missing_content"


def test_score_1_does_not_unlock_score_2_does_and_it_stays(client, clock):
    add_check(client, clock, "py.a.one", level=1)  # level-1 check: no tested_out
    assert not entry(client, "py.a.two")["unlocked"]
    add_check(client, clock, "py.a.one", level=2)
    assert row(client, "py.a.one").score == 2
    two = entry(client, "py.a.two")
    assert two["unlocked"] and two["status"] == "unlocked" and two["lock_reasons"] == []
    at = row(client, "py.a.two").unlocked_at
    assert at is not None
    # prerequisite score falls back: still unlocked, unlocked_at untouched, no reasons
    drop_checks(client, clock, "py.a.one")
    assert row(client, "py.a.one").score < 2
    again = entry(client, "py.a.two")
    assert again["unlocked"] and again["lock_reasons"] == []
    assert row(client, "py.a.two").unlocked_at == at
    # and recomputing everything later does not clear or move it either
    clock.advance(days=3)
    rt = client.app.state.rt
    with rt.session() as db:
        progress.recompute_all(db, rt.content, clock())
        db.commit()
    assert row(client, "py.a.two").unlocked_at == at


def test_tested_out_unlocks_the_subtopic_itself(client, clock):
    assert not entry(client, "py.a.two")["unlocked"]
    add_check(client, clock, "py.a.two", level=2)
    r = row(client, "py.a.two")
    assert r.tested_out and r.unlocked_at is not None
    two = entry(client, "py.a.two")
    assert two["unlocked"] and two["lock_reasons"] == [] and two["tested_out"] is True
    assert two["status"] in {"done", "in_progress"}
    # its prerequisite is untouched
    assert row(client, "py.a.one").score == 0


def test_newly_unlocked_is_reported_once(client, clock):
    rt = client.app.state.rt
    add_check(client, clock, "py.a.one", level=2)
    with rt.session() as db:
        assert (
            progress.recompute_subtopic(db, rt.content, "py.a.one", clock())["newly_unlocked"] == []
        )
