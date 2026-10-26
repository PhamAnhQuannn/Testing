"""Leitner review API (SPEC 5.4, 5.2 retention_ok): schedule from the real day, queue, scoring."""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select

from app.models import tables as t
from app.services import progress
from app.services import scoring as sc

DAY0 = date(2026, 11, 2)  # T0 (10:00 local) is this day in Asia/Ho_Chi_Minh


def key(n: str) -> dict[str, str]:
    return {"Idempotency-Key": n}


def put_card(client, sid="py.a.one", box=1, due=DAY0, score=None):
    with client.app.state.rt.session() as db:
        db.merge(t.ReviewCard(user_id=1, subtopic_id=sid, box=box, due_on=due))
        if score is not None:
            row = db.get(t.UserSubtopic, (1, sid)) or t.UserSubtopic(user_id=1, subtopic_id=sid)
            row.score = score
            db.merge(row)
        db.commit()


def card(client, sid="py.a.one"):
    with client.app.state.rt.session() as db:
        c = db.get(t.ReviewCard, (1, sid))
        db.expunge(c)
        return c


def goto(clock, day: date):
    """Move the clock to 10:00 local (03:00 UTC) of `day`."""
    clock.now = clock.now.replace(year=day.year, month=day.month, day=day.day)


def review(client, ok=True, sid="py.a.one", **body):
    return client.post(f"/api/review/{sid}/result", json={"success": ok, **body})


def logs(client):
    with client.app.state.rt.session() as db:
        return list(db.scalars(select(t.ReviewLog).order_by(t.ReviewLog.id)))


# ---- schedule ----


def test_30_day_simulation_passes_on_each_due_day(client, clock):
    put_card(client, due=DAY0 + timedelta(days=1))  # created on day 0
    seen = []
    for d in range(0, 61):
        goto(clock, DAY0 + timedelta(days=d))
        c = card(client)
        if c.due_on == DAY0 + timedelta(days=d):
            r = review(client, True, item_kind="recall")
            assert r.status_code == 200, r.text
            seen.append((d, r.json()["box_after"]))
    # D+1/3/7/14/28 then +30 (box 5 stays box 5)
    assert seen == [(1, 2), (3, 3), (7, 4), (14, 5), (28, 5), (58, 5)]


def test_late_review_counts_from_the_real_day(client, clock):
    put_card(client, box=2, due=DAY0)
    goto(clock, DAY0 + timedelta(days=10))  # 10 days late
    r = review(client, True, item_kind="recall").json()
    assert r["box_before"] == 2 and r["box_after"] == 3
    assert r["due_on"] == (DAY0 + timedelta(days=14)).isoformat()  # real day + 4, no debt
    assert card(client).due_on == DAY0 + timedelta(days=14)


def test_fail_goes_to_box_1_and_counts_a_lapse(client, clock):
    put_card(client, box=4, due=DAY0)
    r = review(client, False, item_kind="recall").json()
    assert r["box_after"] == 1 and r["lapses"] == 1
    assert r["due_on"] == (DAY0 + timedelta(days=1)).isoformat()
    c = card(client)
    assert (c.box, c.lapses, c.consecutive_passes) == (1, 1, 0)
    assert c.last_reviewed_at is not None


def test_not_due_and_missing_cards_are_refused(client, clock):
    assert review(client, True, item_kind="recall").status_code == 404
    put_card(client, due=DAY0 + timedelta(days=1))
    r = review(client, True, item_kind="recall")
    assert r.status_code == 409 and r.json()["error"]["code"] == "card_not_due"
    assert logs(client) == []


# ---- queue ----


def test_queue_order_overdue_first_then_low_score_and_no_cap(client, clock):
    put_card(client, "py.a.one", due=DAY0, score=2)
    put_card(client, "py.a.two", due=DAY0, score=1)
    put_card(client, "py.a.three", due=DAY0 - timedelta(days=3), score=3)
    # filler cards for the same 3 subtopics are impossible (PK); the cap is checked below
    q = client.get("/api/review/queue").json()
    assert [c["subtopic_id"] for c in q["cards"]] == ["py.a.three", "py.a.two", "py.a.one"]
    assert q["today"] == DAY0.isoformat() and q["total_due"] == 3 and not q["backlog"]
    assert [c["overdue_days"] for c in q["cards"]] == [3, 0, 0]
    # not due yet: absent
    put_card(client, "py.a.two", due=DAY0 + timedelta(days=1), score=1)
    assert [c["subtopic_id"] for c in client.get("/api/review/queue").json()["cards"]] == [
        "py.a.three",
        "py.a.one",
    ]


def test_queue_has_no_server_side_cap(client):
    # the preset (size 2) is only a hint: all 3 due cards are still returned
    client.put("/api/settings", json={"review_preset": 2})
    for sid in ("py.a.one", "py.a.two", "py.a.three"):
        put_card(client, sid)
    q = client.get("/api/review/queue").json()
    assert len(q["cards"]) == 3
    assert q["short_session"]["size"] == 2 and len(q["short_session"]["cards"]) == 2
    client.put("/api/settings", json={"review_preset": None})
    q = client.get("/api/review/queue").json()
    assert len(q["cards"]) == 3 and q["short_session"]["enabled"] is False


def test_queue_item_by_box_and_short_session_code_limit(client):
    put_card(client, "py.a.one", box=1)
    put_card(client, "py.a.two", box=2)
    q = {c["subtopic_id"]: c for c in client.get("/api/review/queue").json()["cards"]}
    assert q["py.a.one"]["item_kind"] == "recall" and q["py.a.one"]["recall_item"] is None
    assert q["py.a.one"]["item"]["ref"].startswith("py.a.one#")  # a graded lesson block
    assert q["py.a.two"]["item"]["ref"] == "check:py.a.two:R1"  # level-1 read_code check

    put_card(client, "py.a.one", box=3)
    c = next(
        c for c in client.get("/api/review/queue").json()["cards"] if c["subtopic_id"] == "py.a.one"
    )
    assert c["item_kind"] == "code" and c["item"]["ref"] in {"check-q2", "check-q3", "add-two"}
    assert c["recall_item"]["kind"] == "recall"
    # no editor (phone): recall, which does not count for retention_ok
    c = next(
        c
        for c in client.get("/api/review/queue?editor=false").json()["cards"]
        if c["subtopic_id"] == "py.a.one"
    )
    assert c["item_kind"] == "recall"


def test_short_session_allows_at_most_two_code_cards(client):
    # three code cards would need three subtopics with problems; only py.a.one has them, so fake
    # the cards list through the pure helper
    from app.services.review import _short_session

    cards = [
        {"subtopic_id": f"s{i}", "item_kind": "code", "recall_item": {"kind": "recall"}}
        for i in range(4)
    ] + [{"subtopic_id": "r", "item_kind": "recall", "recall_item": None}]
    out = _short_session(cards, 5)
    assert [c["item_kind"] for c in out["cards"]] == ["code", "code", "recall", "recall", "recall"]
    assert out["max_code"] == 2 and out["size"] == 5


def test_backlog_flag(client):
    client.put("/api/settings", json={"backlog_warn": 2})
    for sid in ("py.a.one", "py.a.two", "py.a.three"):
        put_card(client, sid)
    q = client.get("/api/review/queue").json()
    assert q["backlog"] is True and q["backlog_warn"] == 2


# ---- review_log / idempotency ----


def test_idempotent_replay_writes_one_log_row(client, clock):
    put_card(client, box=3, due=DAY0)
    body = {"success": True, "item_kind": "recall"}
    a = client.post("/api/review/py.a.one/result", json=body, headers=key("k1"))
    b = client.post("/api/review/py.a.one/result", json=body, headers=key("k1"))
    assert a.status_code == 200 and b.status_code == 200 and a.json() == b.json()
    assert b.headers.get("idempotent-replay") == "true"
    assert len(logs(client)) == 1 and card(client).box == 4


def test_log_records_box_kind_and_ref(client):
    put_card(client, box=3, due=DAY0)
    r = review(client, True, item_ref="check-q2").json()
    assert r["item_kind"] == "code"
    (row,) = logs(client)
    assert (row.item_ref, row.item_kind, row.box_before, row.box_after, row.success) == (
        "check-q2",
        "code",
        3,
        4,
        True,
    )
    # kind mismatch and missing fields
    put_card(client, box=3, due=DAY0)
    assert review(client, True, item_ref="check-q2", item_kind="recall").status_code == 422
    assert review(client, True).status_code == 422
    assert review(client, True, item_kind="recall", item_ref="py.a.one#q1").status_code == 200


# ---- retention_ok end to end ----


def _test_out_score_2(client):
    """Test out (clean level 2 + 3 pass) -> score 2 with a review card (see test_api_checks)."""
    s = client.post("/api/checks/py.a.one/start", json={"context": "test_out"}).json()
    for item in ("Q2", "Q3"):
        r = client.post(
            "/api/checks/py.a.one/answer",
            json={
                "session_id": s["session_id"],
                "item_id": item,
                "elapsed_ms": 60_000,
                "code": "def add(a, b): return a + b",
                "verdict": "AC",
                "passed_tests": 1,
                "total": 1,
            },
        )
        assert r.status_code == 200
    with client.app.state.rt.session() as db:
        assert db.get(t.UserSubtopic, (1, "py.a.one")).score == 2


def _score(client):
    rt = client.app.state.rt
    with rt.session() as db:
        cached = db.get(t.UserSubtopic, (1, "py.a.one")).score
        ev = progress.load_evidence(db, rt.content, "py.a.one")
        res = sc.score(rt.content.spec_for("py.a.one"), ev)
        assert cached == res.score  # parity: the cache equals scoring(events)
        return cached, res.retention_ok


def _climb_to_box(client, clock, box):
    while card(client).box < box:
        goto(clock, card(client).due_on)
        assert review(client, True, item_kind="recall").status_code == 200


def test_retention_ok_only_from_a_code_pass_at_box_3_or_more(client, clock):
    _test_out_score_2(client)
    assert card(client).box == 1 and _score(client) == (2, False)

    # recall passes up to and including box 3 -> 4: never retention_ok
    _climb_to_box(client, clock, 4)
    assert _score(client) == (2, False)

    # a FAILED code review at box 4 does not count either
    goto(clock, card(client).due_on)
    r = review(client, False, item_kind="code").json()
    assert r["box_after"] == 1 and r["item_kind"] == "code"
    assert _score(client) == (2, False)

    # a code pass below box 3 does not count (box 1 -> 2)
    goto(clock, card(client).due_on)
    assert review(client, True, item_kind="code").json()["box_before"] == 1
    assert _score(client) == (2, False)

    # box 2 -> 3 by recall, then a recall pass at box 3: still no
    goto(clock, card(client).due_on)
    review(client, True, item_kind="recall")
    assert card(client).box == 3
    goto(clock, card(client).due_on)
    r = review(client, True, item_kind="recall").json()
    assert r["box_before"] == 3 and r["score"] == {"before": 2, "after": 2}
    assert _score(client) == (2, False)

    # now box 4: a code pass counts (box_before >= 3 and item_kind == code) -> score 3
    goto(clock, card(client).due_on)
    r = review(client, True, item_kind="code").json()
    assert r["box_before"] == 4 and r["item_kind"] == "code"
    assert r["score"] == {"before": 2, "after": 3}
    assert _score(client) == (3, True)
    kinds = [(x.box_before, x.item_kind, x.success) for x in logs(client)]
    assert (4, "code", True) in kinds
    with client.app.state.rt.session() as db:
        n = db.scalar(
            select(func.count()).select_from(t.Event).where(t.Event.type == "review_result")
        )
    assert n == len(kinds)
