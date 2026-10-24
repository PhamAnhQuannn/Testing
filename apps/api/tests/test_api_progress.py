import json
from datetime import timedelta

from sqlalchemy import func, select

from app.models import tables as t
from app.services import progress, scoring


def key(n: str) -> dict[str, str]:
    return {"Idempotency-Key": n}


def answer(client, block, ans, run=1, k=None):
    return client.post(
        "/api/quiz/answers",
        json={"quiz_item_id": f"py.a.one#{block}", "run_no": run, "answer": ans},
        headers=key(k) if k else {},
    )


def do_quiz(client, correct=(True, True, True, True), run=1):
    """q1,q2 mcq (right answer is b); q3 fill (get); q4 predict (1)."""
    right = {"q1": ["b"], "q2": ["b"], "q3": ["get"], "q4": "1"}
    wrong = {"q1": ["a"], "q2": ["a"], "q3": ["pop"], "q4": "2"}
    for (blk, good), ok in zip(right.items(), correct, strict=True):
        r = answer(client, blk, good if ok else wrong[blk], run)
        assert r.status_code == 200
        assert r.json()["correct"] is ok


def attempt(client, verdict="AC", mode="submit", elapsed=60_000, **kw):
    total = kw.pop("total", 2)
    body = {
        "problem_id": "add-two",
        "mode": mode,
        "code": "def add(a, b): return a + b",
        "verdict": verdict,
        "passed": total if verdict == "AC" else 1,
        "total": total,
        "elapsed_ms": elapsed,
        **kw,
    }
    return client.post("/api/attempts", json=body)


def sub_row(client, sid="py.a.one"):
    rt = client.app.state.rt
    with rt.session() as db:
        return db.get(t.UserSubtopic, (1, sid))


def test_quiz_grading_reveals_answer_and_explanation(client):
    r = answer(client, "q1", ["a"]).json()
    assert r["correct"] is False and r["correct_answer"] == ["b"] and r["explain_md"] == "vì 1"
    assert r["attempt_no"] == 1 and r["first_attempt"] and r["graded"]
    r = answer(client, "q1", ["b"]).json()
    assert r["correct"] and r["attempt_no"] == 2 and not r["first_attempt"]
    assert answer(client, "q3", [" get "]).json()["correct"]  # trimmed
    assert answer(client, "q4", "1\n").json()["correct"]
    assert answer(client, "q4", "1").json()["correct_answer"] == "1"
    assert answer(client, "q1", "a").status_code == 422
    assert answer(client, "b01", ["a"]).json()["error"]["code"] == "not_a_quiz"
    assert answer(client, "zz", ["a"]).status_code == 404
    assert answer(client, "q1", ["a"], run=2).json()["error"]["code"] == "invalid_run"


def test_lesson_done_with_quiz_gives_score_1_and_a_review_card(client, clock):
    do_quiz(client, (True, True, True, False))  # 3/4 = 0.75
    r = client.post("/api/lessons/py.a.one/complete").json()
    assert r["quiz_best"] == 0.75 and r["quiz_passed"] and r["score"] == 1
    assert r["score_before"] == 0 and r["status"] == "in_progress"
    # box 1, due the next local day (T0 is 10:00 on 2026-11-02 in Ho Chi Minh)
    assert r["review_card"] == {"box": 1, "due_on": "2026-11-03"}
    # idempotent by nature: a second call creates no second event
    again = client.post("/api/lessons/py.a.one/complete").json()
    assert again["score"] == 1 and again["score_before"] == 1
    rt = client.app.state.rt
    with rt.session() as db:
        n = db.scalar(
            select(func.count()).select_from(t.Event).where(t.Event.type == "lesson_done")
        )
        assert n == 1
    m = client.get("/api/map").json()["subtopics"]
    assert m[0]["score"] == 1 and m[0]["lesson_done"] and m[0]["quiz_best"] == 0.75


def test_lesson_done_with_failed_quiz_is_score_0(client):
    do_quiz(client, (True, False, False, False))
    r = client.post("/api/lessons/py.a.one/complete").json()
    assert r["score"] == 0 and not r["quiz_passed"] and r["review_card"] is None
    # redo the lesson from the start: a better second run lifts the score
    run = client.post("/api/lessons/py.a.one/runs").json()["run_no"]
    assert run == 2
    assert client.get("/api/lessons/py.a.one").json()["progress"]["run_no"] == 2
    do_quiz(client, (True, True, True, True), run=2)
    assert client.get("/api/lessons/py.a.one").json()["progress"]["answers"].keys() == {
        "q1",
        "q2",
        "q3",
        "q4",
    }
    bests = client.post(
        "/api/quiz/answers", json={"quiz_item_id": "py.a.one#q1", "run_no": 2, "answer": ["b"]}
    ).json()
    assert bests["quiz_best"] == 1.0
    # lesson was already marked done in run 1; the cache must follow the events
    rt = client.app.state.rt
    with rt.session() as db:
        progress.recompute_subtopic(db, rt.content, "py.a.one", rt.clock())
        db.commit()
    assert sub_row(client).score == 1


def test_run_numbers_are_per_lesson_and_increase(client):
    assert client.post("/api/lessons/py.a.one/runs").json() == {"run_no": 2}
    assert client.post("/api/lessons/py.a.one/runs").json() == {"run_no": 3}
    assert client.post("/api/lessons/py.a.two/runs").status_code == 404


def test_attempt_ac_clean_and_records_elapsed(client):
    client.post("/api/problems/add-two/start-submit")
    r = attempt(client, elapsed=61_000, runtime_ms=12).json()
    assert r["ac"] and r["clean"] and r["elapsed_ms"] == 61_000
    assert r["score"]["subtopic_id"] == "py.a.one" and r["score"]["after"] == 0
    p = client.get("/api/problems/add-two").json()
    assert p["status"] == "solved" and p["solved_clean"]
    assert p["last_attempt"]["verdict"] == "AC" and p["last_attempt"]["passed"] == 2
    with client.app.state.rt.session() as db:
        a = db.scalars(select(t.Attempt)).one()
        assert a.elapsed_ms == 61_000 and a.clean and a.problem_version == 1


def test_clean_rules(client):
    # too slow: > 1.5 x 10 min
    r = attempt(client, elapsed=15 * 60_000 + 1).json()
    assert r["ac"] and not r["clean"]
    assert attempt(client, elapsed=15 * 60_000).json()["clean"]
    # two hints break it, one does not
    h1 = client.post("/api/problems/add-two/hints").json()
    assert h1["hint"] == "h1" and h1["hints_used"] == 1
    assert attempt(client).json()["clean"]
    h2 = client.post("/api/problems/add-two/hints").json()
    assert h2["hints"] == ["h1", "h2"]
    assert not attempt(client).json()["clean"]
    assert client.get("/api/problems/add-two").json()["hints"] == ["h1", "h2"]
    client.post("/api/problems/add-two/hints")
    last = client.post("/api/problems/add-two/hints").json()
    assert last["hints_used"] == 3 and last["exhausted"] and last["hint"] is None


def test_viewing_the_solution_breaks_clean(client):
    sol = client.get("/api/problems/add-two/solution").json()
    assert "return a + b" in sol["code"] and sol["complexity"] == "O(1)"
    p = client.get("/api/problems/add-two").json()
    assert p["solution_viewed"]
    r = attempt(client).json()
    assert r["ac"] and not r["clean"] and r["solution_viewed"]


def test_wrong_attempts_and_run_mode_do_not_count(client):
    assert not attempt(client, "WA").json()["ac"]
    r = attempt(client, mode="run", verdict="AC").json()
    assert not r["ac"] and r["score"] is None and not r["clean"]
    assert client.get("/api/problems/add-two").json()["status"] == "attempted"
    assert attempt(client, "AC", passed=1).status_code == 422  # AC needs passed == total
    assert attempt(client, "WA", total=1, passed=5).status_code == 422


def test_score_equals_recompute_from_events(client):
    """The cache column always equals scoring(events)."""
    do_quiz(client)
    client.post("/api/lessons/py.a.one/complete")
    attempt(client)
    rt = client.app.state.rt
    with rt.session() as db:
        for sid in rt.content.subtopics:
            cached = db.get(t.UserSubtopic, (1, sid)).score
            ev = progress.load_evidence(db, rt.content, sid)
            assert cached == scoring.score(rt.content.spec_for(sid), ev).score
        # wipe the cache and rebuild it from the event tables
        for r in db.scalars(select(t.UserSubtopic)):
            r.score = 99
        progress.recompute_all(db, rt.content, rt.clock())
        assert db.get(t.UserSubtopic, (1, "py.a.one")).score == 1


def test_score_2_unlocks_dependents_one_way(client, clock):
    """Score 2 through a clean check (inserted directly: checks are M2) unlocks the next item."""
    rt = client.app.state.rt
    do_quiz(client)
    client.post("/api/lessons/py.a.one/complete")
    attempt(client)

    def two():
        return next(s for s in client.get("/api/map").json()["subtopics"] if s["id"] == "py.a.two")

    assert not two()["unlocked"]
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
    assert sub_row(client).score == 2
    assert two()["unlocked"] and two()["status"] == "unlocked"
    unlocked_at = sub_row(client, "py.a.two").unlocked_at
    assert unlocked_at is not None
    # even if the evidence is later removed (content fixed, rows deleted...) it stays unlocked
    with rt.session() as db:
        db.query(t.CheckResult).delete()
        progress.recompute_subtopic(db, rt.content, "py.a.one", clock())
        db.commit()
    assert sub_row(client).score == 1
    assert two()["unlocked"] and sub_row(client, "py.a.two").unlocked_at == unlocked_at


def test_drafts_newer_wins_and_elapsed_is_max(client):
    base = {
        "code": "v1",
        "updated_at": "2026-11-02T03:00:00Z",
        "elapsed_ms": 5000,
        "cursor": {"line": 1, "ch": 2},
    }
    r = client.put("/api/drafts/add-two", json=base).json()
    assert r["accepted"] and r["draft"]["rev"] == 1
    newer = {**base, "code": "v2", "updated_at": "2026-11-02T03:00:02Z", "elapsed_ms": 7000}
    r = client.put("/api/drafts/add-two", json=newer).json()
    assert r["accepted"] and r["draft"]["code"] == "v2" and r["draft"]["rev"] == 2
    stale = {**base, "code": "old", "elapsed_ms": 6000}
    r = client.put("/api/drafts/add-two", json=stale).json()
    assert not r["accepted"] and r["draft"]["code"] == "v2" and r["draft"]["elapsed_ms"] == 7000
    same = client.put("/api/drafts/add-two", json=newer).json()
    assert same["draft"]["rev"] == 2  # identical resend is a no-op
    got = client.get("/api/drafts/add-two").json()["draft"]
    assert got["code"] == "v2" and got["cursor"] == {"line": 1, "ch": 2} and got["started_at"]
    assert client.get("/api/drafts/add-two", params={"language": "java"}).json() == {"draft": None}
    assert client.put("/api/drafts/none", json=base).status_code == 404


def test_attempt_takes_started_at_from_the_draft(client):
    client.put(
        "/api/drafts/add-two",
        json={
            "code": "x",
            "updated_at": "2026-11-02T03:00:00Z",
            "started_at": "2026-11-02T02:50:00Z",
        },
    )
    attempt(client)
    with client.app.state.rt.session() as db:
        a = db.scalars(select(t.Attempt)).one()
        assert a.started_at.isoformat().startswith("2026-11-02T02:50:00")


def test_occurred_at_is_clamped(client, clock):
    far_past = "2020-01-01T00:00:00Z"
    attempt(client, occurred_at=far_past)
    far_future = "2099-01-01T00:00:00Z"
    attempt(client, occurred_at=far_future)
    with client.app.state.rt.session() as db:
        times = [a.submitted_at for a in db.scalars(select(t.Attempt).order_by(t.Attempt.id))]
        assert times[0] == clock() - timedelta(days=7)
        assert times[1] == clock() + timedelta(minutes=5)
        ev = db.scalars(select(t.Event)).first()
        assert ev.received_at == clock() and ev.occurred_at != ev.received_at


def test_resume_roundtrip(client, clock):
    assert client.get("/api/resume").json() == {
        "primary": None,
        "others": [],
        "in_progress": {"placement": None, "check": None, "review": None},
    }
    body = {
        "mode": "lesson",
        "route": "/s/py.a.one",
        "ref": {
            "subtopic_id": "py.a.one",
            "block_id": "q2",
            "scroll_in_block": 0.4,
            "tab": "lesson",
        },
        "device_id": "d1",
    }
    assert client.put("/api/resume", json=body).json() == {"ok": True}
    r = client.get("/api/resume").json()
    assert r["primary"]["ref"]["block_id"] == "q2" and r["primary"]["stale"] is False
    # sendBeacon: POST with a text/plain body
    beacon = {**body, "ref": {"subtopic_id": "py.a.one", "block_id": "q3"}}
    clock.advance(seconds=5)
    resp = client.post(
        "/api/resume", content=json.dumps(beacon), headers={"content-type": "text/plain"}
    )
    assert resp.status_code == 200
    assert client.get("/api/resume").json()["primary"]["ref"]["block_id"] == "q3"
    # a late, older write never overwrites a newer position
    client.put("/api/resume", json={**body, "updated_at": "2026-11-02T00:00:00Z"})
    assert client.get("/api/resume").json()["primary"]["ref"]["block_id"] == "q3"
    assert client.post("/api/resume", content="{not json").status_code == 422


def test_resume_problem_goes_stale_after_ac_and_lists_in_progress_lessons(client, clock):
    client.put(
        "/api/resume",
        json={"mode": "problem", "route": "/p/add-two", "ref": {"problem_id": "add-two"}},
    )
    clock.advance(minutes=1)
    answer(client, "q1", ["b"])  # py.a.one becomes in_progress
    assert client.get("/api/resume").json()["primary"]["stale"] is False
    attempt(client)
    r = client.get("/api/resume").json()
    assert r["primary"]["stale"] is True
    assert [o["ref"]["subtopic_id"] for o in r["others"]] == ["py.a.one"]


def test_me_and_settings(client):
    me = client.get("/api/me").json()
    assert me["user"] == {"id": 1, "name": "Quan"}
    assert me["settings"]["tz"] == "Asia/Ho_Chi_Minh" and me["settings"]["review_preset"] == 6
    assert me["onboarding"] == {"profile_done": False, "placement": "none"}
    s = client.put("/api/settings", json={"backlog_warn": 30, "review_preset": None}).json()
    assert s["backlog_warn"] == 30 and s["review_preset"] is None and s["tz"] == "Asia/Ho_Chi_Minh"
    assert (
        client.put("/api/settings", json={"tz": "Mars/Base"}).json()["error"]["code"]
        == "invalid_tz"
    )
    assert client.put("/api/settings", json={"tz": "UTC"}).json()["tz"] == "UTC"


def test_error_shape(client):
    r = client.post("/api/attempts", json={})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"
    r = client.get("/api/nothing")
    assert r.status_code == 404 and r.json()["error"]["code"] == "http_404"
