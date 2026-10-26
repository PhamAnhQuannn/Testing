"""Hoc tiep (SPEC 5.5) and the activity ping / study_time (SPEC 6.4)."""

from __future__ import annotations

from datetime import date

from sqlalchemy import select

from app.models import tables as t
from app.services import progress
from tests.test_api_progress import attempt, do_quiz


def ids(rows):
    return [r["id"] for r in rows]


def lesson_done(client):
    do_quiz(client)
    client.post("/api/lessons/py.a.one/complete")


def raise_to_2(client, clock):
    rt = client.app.state.rt
    attempt(client)
    with rt.session() as db:
        db.add(
            t.CheckResult(
                user_id=1,
                subtopic_id="py.a.one",
                item_id="Q2",
                level=2,
                passed=True,
                clean=True,
                taken_at=clock(),
                item_type="write_code",
            )
        )
        progress.recompute_subtopic(db, rt.content, "py.a.one", clock())
        db.commit()


def set_rows(client, sid, **kw):
    with client.app.state.rt.session() as db:
        row = db.get(t.UserSubtopic, (1, sid))
        for k, v in kw.items():
            setattr(row, k, v)
        db.commit()


def test_fresh_user_sees_the_first_unlocked_item_and_no_must_raise(client):
    n = client.get("/api/next").json()
    assert ids(n["up_next"]) == ["py.a.one"]
    assert n["up_next"][0]["status"] == "unlocked"
    assert n["up_next"][0]["suggested_problem"]["id"] == "add-two"
    assert n["must_raise"] == []
    assert ids(n["locked_preview"]) == ["py.a.two", "py.a.three"]
    assert n["locked_preview"][0]["lock_reasons"][0]["prerequisite"] == "py.a.one"
    assert n["due_count"] == 0 and n["backlog"] is False
    assert n["study"] == {"today_s": 0, "week_s": 0}
    # no schedule vocabulary anywhere
    text = str(n).lower()
    for word in ("late", "trễ", "quota", "streak", "plan_day", "current_day"):
        assert word not in text


def test_started_prerequisite_below_2_is_must_raise(client):
    lesson_done(client)  # py.a.one score 1; its target_intern is 2, so not done
    n = client.get("/api/next").json()
    assert ids(n["up_next"]) == ["py.a.one"]
    assert n["up_next"][0]["status"] == "in_progress" and n["up_next"][0]["score"] == 1
    [m] = n["must_raise"]
    assert m["prerequisite"] == {"id": "py.a.one", "name_vi": "Mục py.a.one", "score": 1, "need": 2}
    assert m["unlocks"]["id"] == "py.a.two" and m["sole_blocker"] is True
    assert m["test_out"]["available"] is True and m["test_out"]["retry_after"] is None
    assert m["suggested_problem"]["id"] == "add-two"
    assert n["due_count"] == 0  # the D+1 card is not due yet


def test_done_item_leaves_up_next_and_the_next_one_comes_up(client, clock):
    lesson_done(client)
    raise_to_2(client, clock)
    n = client.get("/api/next").json()
    assert ids(n["up_next"]) == ["py.a.two"]
    assert n["must_raise"] == []
    assert n["up_next"][0]["suggested_problem"] is None  # it has no problem in the content


def test_target_1_item_is_done_at_score_1_but_still_blocks_dependents(client):
    # memory_model case of SPEC 5.5: done at 1 (target_intern 1), a dependent still needs 2
    client.app.state.rt.content.subtopics["py.a.one"]["target_swe"]["intern"] = 1
    lesson_done(client)
    n = client.get("/api/next").json()
    assert "py.a.one" not in ids(n["up_next"])
    assert [m["prerequisite"]["id"] for m in n["must_raise"]] == ["py.a.one"]


def test_in_progress_first_then_plan_order_then_check_retry_locked_last(client, clock):
    # unlock two and three by hand (they stay unlocked once unlocked_at is set)
    set_rows(client, "py.a.two", unlocked_at=clock(), score=1, status="in_progress")
    set_rows(client, "py.a.three", unlocked_at=clock())
    n = client.get("/api/next").json()
    # two is in progress: first, though one precedes it in plan order
    assert ids(n["up_next"]) == ["py.a.two", "py.a.one", "py.a.three"]
    # a failed check on two (24 h lock) moves it after the items that can be done right now
    with client.app.state.rt.session() as db:
        db.add(
            t.CheckResult(
                user_id=1,
                subtopic_id="py.a.two",
                item_id="R2",
                level=2,
                passed=False,
                clean=False,
                taken_at=clock(),
                item_type="read_code",
            )
        )
        db.commit()
    n = client.get("/api/next").json()
    assert ids(n["up_next"]) == ["py.a.one", "py.a.three", "py.a.two"]
    assert n["up_next"][-1]["check_retry_after"] is not None
    clock.advance(hours=25)
    assert ids(client.get("/api/next").json()["up_next"])[0] == "py.a.two"


def test_due_count_and_backlog(client, clock):
    lesson_done(client)
    clock.advance(days=1)
    n = client.get("/api/next").json()
    assert n["due_count"] == 1 and n["backlog"] is False
    client.put("/api/settings", json={"backlog_warn": 1})
    assert client.get("/api/next").json()["backlog"] is False  # 1 > 1 is false


# ---- activity ping ----


def study(client):
    with client.app.state.rt.session() as db:
        return {r.day: r.seconds for r in db.scalars(select(t.StudyTime))}


def test_first_ping_adds_nothing_then_gaps_are_capped_at_60s(client, clock):
    r = client.post("/api/activity/ping").json()
    assert r == {"added_s": 0, "today_s": 0, "week_s": 0}
    clock.advance(seconds=30)
    assert client.post("/api/activity/ping").json()["added_s"] == 30
    clock.advance(seconds=100)  # between 60 s and 2 min: counted as 60
    r = client.post("/api/activity/ping").json()
    assert r["added_s"] == 60 and r["today_s"] == 90
    assert study(client) == {date(2026, 11, 2): 90}


def test_gap_over_two_minutes_is_skipped_and_resets_last_ping(client, clock):
    client.post("/api/activity/ping")
    clock.advance(seconds=121)
    assert client.post("/api/activity/ping").json()["added_s"] == 0
    clock.advance(seconds=20)  # counted from the ping that was skipped
    assert client.post("/api/activity/ping").json()["added_s"] == 20
    clock.advance(seconds=120)  # exactly 2 minutes still counts (capped at 60)
    assert client.post("/api/activity/ping").json()["added_s"] == 60


def test_a_resend_and_two_tabs_never_double_count(client, clock):
    client.post("/api/activity/ping")
    clock.advance(seconds=30)
    assert client.post("/api/activity/ping").json()["added_s"] == 30
    # same instant again (resend, or a second tab): nothing added
    assert client.post("/api/activity/ping").json()["added_s"] == 0
    assert study(client) == {date(2026, 11, 2): 30}


def test_ping_keeps_days_apart_and_reports_the_week(client, clock):
    client.post("/api/activity/ping")
    clock.advance(seconds=45)
    client.post("/api/activity/ping")
    clock.advance(days=1)  # 2026-11-03, same week (Monday 2026-11-02)
    client.post("/api/activity/ping")
    clock.advance(seconds=10)
    r = client.post("/api/activity/ping").json()
    assert r["today_s"] == 10 and r["week_s"] == 55
    assert client.get("/api/next").json()["study"] == {"today_s": 10, "week_s": 55}


def test_ping_can_carry_resume(client):
    body = {
        "resume": {"mode": "lesson", "route": "/s/py.a.one", "ref": {"subtopic_id": "py.a.one"}}
    }
    assert client.post("/api/activity/ping", json=body).status_code == 200
    assert client.get("/api/resume").json()["primary"]["route"] == "/s/py.a.one"
