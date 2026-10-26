"""Mastery check and test out (SPEC 2.3 flows C/D, 5.2, 6.4): ladder, 24 h lock, scoring wiring."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app.models import tables as t
from app.services import progress
from app.services import scoring as sc
from app.services.content_loader import ContentStore

REPO_CONTENT = Path(__file__).resolve().parents[3] / "content"


def sub_row(client, sid="py.a.one"):
    with client.app.state.rt.session() as db:
        return db.get(t.UserSubtopic, (1, sid))


def do_quiz(client, correct=(True, True, True, True)):
    """q1,q2 mcq (right answer is b); q3 fill (get); q4 predict (1)."""
    right = {"q1": ["b"], "q2": ["b"], "q3": ["get"], "q4": "1"}
    wrong = {"q1": ["a"], "q2": ["a"], "q3": ["pop"], "q4": "2"}
    for (blk, good), ok in zip(right.items(), correct, strict=True):
        r = client.post(
            "/api/quiz/answers",
            json={
                "quiz_item_id": f"py.a.one#{blk}",
                "run_no": 1,
                "answer": good if ok else wrong[blk],
            },
        )
        assert r.status_code == 200


def attempt(client, elapsed=60_000):
    """A Submit AC of the practice problem `add-two`."""
    return client.post(
        "/api/attempts",
        json={
            "problem_id": "add-two",
            "mode": "submit",
            "code": "def add(a, b): return a + b",
            "verdict": "AC",
            "passed": 2,
            "total": 2,
            "elapsed_ms": elapsed,
        },
    )


def key(n: str) -> dict[str, str]:
    return {"Idempotency-Key": n}


def start(client, sid="py.a.one", context=None, k=None):
    body = {"context": context} if context else None
    return client.post(f"/api/checks/{sid}/start", json=body, headers=key(k) if k else {})


def write(session, item="Q2", ok=True, elapsed=60_000, **kw):
    return {
        "session_id": session,
        "item_id": item,
        "elapsed_ms": elapsed,
        "code": "def add(a, b): return a + b",
        "verdict": "AC" if ok else "WA",
        "passed_tests": 1 if ok else 0,
        "total": 1,
        **kw,
    }


def answer(client, body, sid="py.a.one", k=None):
    return client.post(f"/api/checks/{sid}/answer", json=body, headers=key(k) if k else {})


def parity(client, sid="py.a.one"):
    """The cached score equals scoring(events) (SPEC 5.2: the cache is only a cache)."""
    rt = client.app.state.rt
    with rt.session() as db:
        cached = db.get(t.UserSubtopic, (1, sid)).score
        ev = progress.load_evidence(db, rt.content, sid)
        assert cached == sc.score(rt.content.spec_for(sid), ev).score
        return cached


def rows(client, model):
    with client.app.state.rt.session() as db:
        return list(db.scalars(select(model).order_by(model.id)))


def learn(client):
    """Lesson done (quiz 3/4 graded blocks >= 0.7) so s1 holds."""
    do_quiz(client, correct=(True, True, True, False))
    assert client.post("/api/lessons/py.a.one/complete").json()["score"] == 1


# ---- start ----


def test_start_serves_the_first_item_without_the_answer(client):
    r = start(client)
    assert r.status_code == 200, r.text
    s = r.json()
    assert (s["attempt_no"], s["resumed"], s["status"], s["context"]) == (
        1,
        False,
        "in_progress",
        "mastery",
    )
    step = s["step"]
    assert (step["item_id"], step["level"], step["type"]) == ("Q2", 2, "write_code")
    assert step["problem_id"] == "check-q2" and step["time_limit_ms"] == 8 * 60_000
    blob = json.dumps(s)
    assert "REFERENCE" not in blob and "rubric" not in blob and "solution" not in blob
    assert client.get("/api/subtopics/py.a.one").json()["checks"][1]["item_id"] == "Q2"
    # the check problem is served to the check flow although it is not `published`
    p = client.get("/api/problems/check-q2").json()
    assert p["kind"] == "check" and "solution" not in p
    assert (
        client.get("/api/problems", params={"subtopic": "py.a.one"}).json()["problems"][0]["id"]
        == "add-two"
    )
    assert len(client.get("/api/problems", params={"subtopic": "py.a.one"}).json()["problems"]) == 1


def test_start_errors(client):
    assert start(client, "nope").json()["error"]["code"] == "subtopic_not_found"
    client.app.state.rt.content.checks["py.a.one"] = []
    assert start(client).json()["error"]["code"] == "check_not_found"


def test_start_resumes_within_24h_and_expires_after(client, clock):
    first = start(client).json()
    clock.advance(hours=23)
    again = start(client).json()
    assert again["resumed"] and again["session_id"] == first["session_id"]
    clock.advance(hours=24)  # idle for 24 h since the resume
    fresh = start(client).json()
    assert not fresh["resumed"] and fresh["session_id"] != first["session_id"]
    old = rows(client, t.CheckSession)[0]
    assert old.status == "expired"
    assert rows(client, t.CheckResult) == []  # expiry is not a failure
    assert fresh["attempt_no"] == 1  # nothing was answered, so the number is not burnt


def test_answer_on_an_expired_session_is_refused(client, clock):
    s = start(client).json()
    clock.advance(hours=25)
    r = answer(client, write(s["session_id"]))
    assert r.status_code == 409 and r.json()["error"]["code"] == "check_session_expired"
    assert (
        client.post(f"/api/checks/{s['session_id']}/heartbeat", json={"elapsed_ms": 5}).status_code
        == 409
    )


# ---- flow D: test out; SPEC 5.2 example 2 ----


def test_test_out_clean_pass_gives_score_2_and_a_one_way_unlock(client, clock):
    two = lambda: sub_row(client, "py.a.two")  # noqa: E731
    assert two().unlocked_at is None
    s = start(client, context="test_out").json()  # never opened the lesson
    r = answer(client, write(s["session_id"], elapsed=60_000)).json()
    assert r["result"]["passed"] and r["result"]["clean"] and not r["finished"]
    assert r["score"]["before"] == 0 and r["score"]["after"] == 2 and r["score"]["tested_out"]
    assert r["next"]["item_id"] == "Q3" and r["next"]["level"] == 3
    row = sub_row(client)
    assert row.score == 2 and row.tested_out and row.unlocked_at is not None  # unlocks itself
    assert two().unlocked_at is not None and r["score"]["newly_unlocked"] == ["py.a.two"]
    with client.app.state.rt.session() as db:
        card = db.get(t.ReviewCard, (1, "py.a.one"))
        assert card is not None and card.box == 1  # review card from the day of the pass

    # level 3 passed too: still 2 (level3_ok but no retention_ok); the session is finished
    r = answer(client, write(s["session_id"], "Q3", elapsed=90_000)).json()
    assert r["finished"] and r["outcome"]["level3"] == "passed" and r["outcome"]["score"] == 2
    assert r["outcome"]["tested_out"] and r["outcome"]["retry_after"] is None
    assert parity(client) == 2
    res = rows(client, t.CheckResult)
    assert [(c.item_id, c.level, c.passed, c.clean, c.context, c.attempt_no) for c in res] == [
        ("Q2", 2, True, True, "test_out", 1),
        ("Q3", 3, True, True, "test_out", 1),
    ]
    # one-way: the evidence going away later never locks it again (SPEC 5.3)
    first_unlock = two().unlocked_at
    rt = client.app.state.rt
    with rt.session() as db:
        db.query(t.CheckResult).delete()
        progress.recompute_subtopic(db, rt.content, "py.a.one", clock())
        db.commit()
    assert sub_row(client).score == 0 and sub_row(client).unlocked_at is not None
    assert two().unlocked_at == first_unlock


def test_a_failed_level_3_locks_level_3_for_24h(client):
    s = start(client).json()
    answer(client, write(s["session_id"]))
    answer(client, write(s["session_id"], "Q3", ok=False))  # level 3 fails: locked for 24 h
    r = start(client)
    assert r.status_code == 409 and r.json()["error"]["code"] == "check_retry_locked"
    assert r.json()["error"]["level"] == 3


def test_a_redo_after_level2_and_3_passed_is_refused(client):
    s = start(client).json()
    answer(client, write(s["session_id"]))
    answer(client, write(s["session_id"], "Q3"))
    r = start(client)
    assert r.status_code == 409 and r.json()["error"]["code"] == "check_already_passed"


def test_a_tested_out_subtopic_restarts_at_level_3(client, clock):
    s = start(client).json()
    answer(client, write(s["session_id"]))
    answer(client, write(s["session_id"], "Q3", ok=False))
    clock.advance(hours=24)
    s2 = start(client).json()
    assert s2["step"]["level"] == 3 and s2["step"]["item_id"] == "Q3" and s2["attempt_no"] == 2


# ---- clean rules (SPEC 5.1) ----


def test_clean_needs_at_most_one_hint_no_solution_and_time(client):
    s = start(client).json()
    sid = s["session_id"]
    for _ in range(2):
        assert client.post("/api/problems/check-q2/hints").status_code == 200
    r = answer(client, write(sid)).json()
    res = r["result"]
    assert res["correct"] and res["passed"] and not res["clean"] and res["reason"] == "hint_limit"
    assert r["score"]["after"] == 0 and not r["score"]["tested_out"]  # not clean: no evidence
    assert r["next"]["level"] == 3  # correct goes UP the ladder, not down to the diagnostic
    assert client.post(f"/api/checks/{sid}/heartbeat", json={"elapsed_ms": 1}).status_code == 200
    # finish the session: no 24 h lock follows a correct answer
    fin = answer(client, write(sid, "Q3")).json()
    assert fin["finished"] and fin["outcome"]["retry_after"] is None
    assert fin["outcome"]["level2"] == "passed" and not fin["outcome"]["tested_out"]
    assert parity(client) == 0
    assert start(client).status_code == 200  # level 2 again at once (it is not clean-passed)


def test_one_hint_is_still_clean_and_time_limit_is_1_5x(client):
    s = start(client).json()
    client.post("/api/problems/check-q2/hints")
    over = answer(client, write(s["session_id"], elapsed=int(1.5 * 8 * 60_000) + 1)).json()
    res = over["result"]
    assert res["reason"] == "over_time" and res["correct"] and res["passed"] and not res["clean"]
    assert over["score"]["after"] == 0 and over["next"]["level"] == 3
    fin = answer(client, write(s["session_id"], "Q3")).json()
    assert fin["outcome"]["retry_after"] is None  # no lock for a correct answer
    # an immediate redo starts again with a fresh hint count; 1 hint at exactly 1.5x is clean
    s2 = start(client).json()
    assert s2["attempt_no"] == 2 and s2["step"]["level"] == 2
    client.post("/api/problems/check-q2/hints")
    ok = answer(client, write(s2["session_id"], elapsed=int(1.5 * 8 * 60_000))).json()
    assert ok["result"]["clean"] and ok["score"]["after"] == 2


def test_viewing_the_solution_is_not_clean(client):
    s = start(client).json()
    # the reference is locked while the check is not passed, so view it via the practice route
    assert client.get("/api/problems/check-q2/solution").status_code == 403
    rt = client.app.state.rt
    with rt.session() as db:
        db.merge(
            t.ProblemState(user_id=1, problem_id="check-q2", hints_used=0, solution_viewed=True)
        )
        db.commit()
    r = answer(client, write(s["session_id"])).json()
    assert r["result"]["reason"] == "solution_viewed" and r["score"]["after"] == 0
    assert r["result"]["correct"] and r["result"]["passed"] and not r["result"]["clean"]
    assert r["next"]["level"] == 3 and not r["score"]["tested_out"]


# ---- fail: no reference, 24 h lock; SPEC 5.2 example 3 ----


def test_fail_does_not_leak_the_reference_and_locks_for_24h(client, clock):
    s = start(client).json()
    sid = s["session_id"]
    r = answer(client, write(sid, ok=False), k="k-fail")
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["passed"] is False and body["result"]["verdict"] == "WA"
    assert body["next"]["item_id"] == "Q1" and body["next"]["level"] == 1  # diagnostic
    blob = json.dumps(body)
    assert "REFERENCE" not in blob and "return a + b" not in blob
    assert (
        client.get("/api/problems/check-q2/solution").json()["error"]["code"]
        == "check_solution_locked"
    )

    # level 1 (concept, self-graded) closes the session; it never raises the score
    r = answer(client, {"session_id": sid, "item_id": "Q1", "self_grade": True}).json()
    assert (
        r["finished"] and r["outcome"]["level1"] == "passed" and r["outcome"]["level2"] == "failed"
    )
    assert r["score"]["after"] == 0 and not r["outcome"]["need_lesson"]
    retry = r["outcome"]["retry_after"]

    locked = start(client)
    assert locked.status_code == 409
    err = locked.json()["error"]
    assert err["code"] == "check_retry_locked" and err["retry_after"] == retry
    clock.advance(hours=23, minutes=59)
    assert start(client).json()["error"]["code"] == "check_retry_locked"
    clock.advance(minutes=1)
    s2 = start(client)
    assert s2.status_code == 200 and s2.json()["attempt_no"] == 2
    assert [c.attempt_no for c in rows(client, t.CheckResult)] == [1, 1]
    assert parity(client) == 0


def test_example_3_failed_then_practice_exit_gives_2(client, clock):
    learn(client)
    s = start(client).json()
    answer(client, write(s["session_id"], ok=False))
    assert start(client).json()["resumed"]  # still the same session (level 1 pending)
    answer(client, {"session_id": s["session_id"], "item_id": "Q1", "self_grade": False})
    assert start(client).json()["error"]["code"] == "check_retry_locked"
    clock.advance(days=1)
    # next day: a clean practice AC after a failed level 2 is the exit (only 1 practice problem)
    r = attempt(client).json()
    assert r["clean"] and r["score"]["before"] == 1 and r["score"]["after"] == 2
    row = sub_row(client)
    assert row.score == 2 and not row.tested_out  # score 2 without passing the check
    assert parity(client) == 2


def test_gave_up_is_recorded_but_does_not_lock_or_open_the_exit(client):
    learn(client)
    s = start(client).json()
    r = answer(client, {"session_id": s["session_id"], "item_id": "Q2", "gave_up": True}).json()
    assert r["result"]["gave_up"] and not r["result"]["passed"] and r["next"]["level"] == 1
    answer(client, {"session_id": s["session_id"], "item_id": "Q1", "self_grade": False})
    again = start(client)
    assert again.status_code == 200  # not locked: gave_up does not count as a failure
    assert attempt(client).json()["score"]["after"] == 1  # and the practice exit stays closed
    assert parity(client) == 1


# ---- worked example 1 through the API: the D1 fallback is gone ----


def test_example_1_clean_practice_ac_alone_is_not_score_2_any_more(client):
    learn(client)  # day 2: score 1
    r = attempt(client).json()  # AC clean in 1 min: practice_ok, but there is a level 2 check now
    assert r["clean"] and r["score"]["after"] == 1
    assert sub_row(client).score == 1
    s = start(client).json()  # day 3
    a = answer(client, write(s["session_id"], elapsed=5 * 60_000)).json()
    assert a["score"]["after"] == 2  # passing the check is what gives score 2
    b = answer(client, write(s["session_id"], "Q3", elapsed=9 * 60_000)).json()
    assert b["finished"] and b["score"]["after"] == 2  # level3_ok but not retention_ok
    assert parity(client) == 2


def test_the_loader_takes_check_levels_from_content_checks(client):
    """Hand-written lessons have empty `mastery_check`; the check files still decide."""
    content = client.app.state.rt.content
    content.lessons["py.a.one"].data["mastery_check"] = {"l1": [], "l2": [], "l3": []}
    spec = content.spec_for("py.a.one")
    assert spec.has_l2_items and spec.has_l3_write_code
    learn(client)
    assert attempt(client).json()["score"]["after"] == 1


def _add_sibling_l2(client):
    """A second level-2 write_code item that sorts FIRST (like Q006 before X003)."""
    content = client.app.state.rt.content
    sibling = {**content.checks["py.a.one"][1], "id": "Q2b"}
    content.checks["py.a.one"].insert(0, sibling)
    return content


@pytest.mark.parametrize("context", ["mastery", "test_out"])
def test_the_ladder_serves_the_lessons_curated_mastery_check_item(client, context):
    content = _add_sibling_l2(client)  # lesson mastery_check.l2 == ["Q2"]
    assert content.check_items("py.a.one")[2][0]["id"] == "Q2b"
    assert start(client, "py.a.one", context).json()["step"]["item_id"] == "Q2"


def test_without_a_curated_list_the_ladder_uses_all_items_of_the_level(client):
    content = _add_sibling_l2(client)
    content.lessons["py.a.one"].data["mastery_check"] = {"l1": [], "l2": [], "l3": []}
    assert start(client).json()["step"]["item_id"] == "Q2b"


def test_real_content_has_levels_from_the_check_files():
    store = ContentStore.load(REPO_CONTENT)
    spec = store.spec_for("py.datastructs.dict")
    assert spec.has_l2_items and spec.has_l3_write_code  # Q023 / Q024
    ev = sc.Evidence(
        lesson_done=True,
        quiz_answers=tuple(sc.QuizAnswerEv(q, 1, 1, True) for q in spec.graded_quiz_ids),
        attempts=tuple(sc.AttemptEv(p, True, True) for p in spec.practice_ids),
    )
    assert sc.score(spec, ev).score == 1  # a clean practice AC is no longer enough


# ---- item types ----


def test_read_code_is_graded_on_the_server_and_hides_the_answer(client):
    s = start(client, "py.a.two", "test_out").json()
    step = s["step"]
    assert (step["item_id"], step["type"], step["code"]) == ("R2", "read_code", "print(2)")
    assert "expected_output" not in json.dumps(s) and "two" not in json.dumps(s["step"]).replace(
        "print", ""
    )
    wrong = answer(
        client, {"session_id": s["session_id"], "item_id": "R2", "answer": "3"}, "py.a.two"
    ).json()
    assert not wrong["result"]["passed"] and wrong["result"]["reason"] == "wrong_answer"
    assert "expected" not in json.dumps(wrong) and wrong["next"]["item_id"] == "R1"
    assert wrong["score"]["after"] == 0

    clock_ok = start(client, "py.a.two")  # level 1 is pending in the same session
    assert clock_ok.json()["resumed"]


def test_read_code_pass_counts_and_a_concept_level_3_does_not_add_score(client):
    s = start(client, "py.a.two", "test_out").json()
    r = answer(
        client, {"session_id": s["session_id"], "item_id": "R2", "answer": " 2 \n"}, "py.a.two"
    ).json()
    assert r["result"]["passed"] and r["score"]["after"] == 2
    assert r["next"] == {**r["next"], "item_id": "C3", "level": 3, "type": "concept"}
    r = answer(
        client, {"session_id": s["session_id"], "item_id": "C3", "self_grade": True}, "py.a.two"
    ).json()
    assert r["finished"] and r["outcome"]["level3"] == "passed" and r["score"]["after"] == 2
    assert parity(client, "py.a.two") == 2


def test_concept_is_never_evidence_for_score_2(client):
    s = start(client, "py.a.three", "test_out").json()
    assert s["step"]["type"] == "concept" and s["step"]["answer_md"] == "x"
    r = answer(
        client, {"session_id": s["session_id"], "item_id": "C2", "self_grade": True}, "py.a.three"
    ).json()
    assert r["result"]["passed"] and not r["result"]["clean"]
    assert r["score"]["after"] == 0 and not r["score"]["tested_out"]
    assert r["finished"]  # no level 3 item, and the pass needs no diagnostic
    [res] = rows(client, t.CheckResult)
    assert (res.item_type, res.passed, res.clean) == ("concept", True, False)
    assert parity(client, "py.a.three") == 0
    row = sub_row(client, "py.a.three")
    assert row.score == 0 and not row.tested_out and row.unlocked_at is None


def test_no_level_1_item_means_learn_the_lesson(client):
    s = start(client, "py.a.three").json()
    r = answer(
        client, {"session_id": s["session_id"], "item_id": "C2", "self_grade": False}, "py.a.three"
    ).json()
    assert r["finished"] and r["outcome"]["need_lesson"] and r["outcome"]["level2"] == "failed"
    assert r["outcome"]["retry_after"] is not None


# ---- request validation and heartbeat ----


def test_answer_validation(client):
    s = start(client).json()
    sid = s["session_id"]
    assert answer(client, write(sid, "Q3")).json()["error"]["code"] == "check_wrong_item"
    assert answer(client, write(999)).json()["error"]["code"] == "check_session_not_found"
    assert (
        answer(client, write(sid), "py.a.two").json()["error"]["code"] == "check_session_not_found"
    )
    assert (
        answer(client, {"session_id": sid, "item_id": "Q2"}).json()["error"]["code"]
        == "missing_field"
    )
    assert (
        answer(client, write(sid, passed_tests=3, total=1)).json()["error"]["code"]
        == "invalid_counts"
    )
    assert (
        answer(client, write(sid, verdict="AC", passed_tests=0)).json()["error"]["code"]
        == "invalid_counts"
    )
    assert answer(client, write(sid, elapsed_ms=-1)).status_code == 422
    answer(client, write(sid, ok=False))
    answer(client, {"session_id": sid, "item_id": "Q1", "self_grade": True})
    assert answer(client, write(sid)).json()["error"]["code"] == "check_session_done"


def test_heartbeat_is_absolute_and_safe_to_resend(client, clock):
    sid = start(client).json()["session_id"]
    hb = lambda ms: client.post(f"/api/checks/{sid}/heartbeat", json={"elapsed_ms": ms}).json()  # noqa: E731
    assert hb(5_000)["elapsed_ms"] == 5_000
    assert hb(5_000)["elapsed_ms"] == 5_000
    assert hb(3_000)["elapsed_ms"] == 5_000  # the clock only moves forward
    clock.advance(hours=1)
    assert hb(9_000)["status"] == "in_progress"
    s = start(client).json()
    assert s["resumed"] and s["elapsed_ms"] == 9_000
    assert client.post("/api/checks/777/heartbeat", json={"elapsed_ms": 1}).status_code == 404


# ---- idempotency ----


def test_replaying_an_answer_with_the_same_key_writes_once(client):
    sid = start(client).json()["session_id"]
    first = answer(client, write(sid), k="ans-1")
    again = answer(client, write(sid), k="ans-1")
    assert first.status_code == again.status_code == 200
    assert again.json() == first.json() and again.headers["idempotent-replay"] == "true"
    assert len(rows(client, t.CheckResult)) == 1
    with client.app.state.rt.session() as db:
        n = db.scalar(
            select(func.count()).select_from(t.Attempt).where(t.Attempt.problem_id == "check-q2")
        )
        ev = db.scalar(
            select(func.count()).select_from(t.Event).where(t.Event.type == "check_item_result")
        )
    assert n == 1 and ev == 1
    # without the key the same answer is a conflict, not a second result
    assert answer(client, write(sid)).json()["error"]["code"] == "check_wrong_item"
    assert len(rows(client, t.CheckResult)) == 1


def test_replaying_start_with_the_same_key_returns_the_same_session(client):
    a = start(client, k="st-1")
    b = start(client, k="st-1")
    assert a.json() == b.json() and b.headers["idempotent-replay"] == "true"
    assert len(rows(client, t.CheckSession)) == 1


def test_score_cache_always_matches_the_events_after_any_sequence(client, clock):
    learn(client)
    s = start(client).json()
    answer(client, write(s["session_id"], ok=False))
    parity(client)
    answer(client, {"session_id": s["session_id"], "item_id": "Q1", "self_grade": True})
    parity(client)
    clock.advance(days=1)
    s = start(client).json()
    answer(client, write(s["session_id"]))
    answer(client, write(s["session_id"], "Q3", ok=False))
    assert parity(client) == 2
    rt = client.app.state.rt
    with rt.session() as db:
        for r in db.scalars(select(t.UserSubtopic)):
            r.score = 99
        progress.recompute_all(db, rt.content, clock())
        db.commit()
    assert sub_row(client).score == 2
