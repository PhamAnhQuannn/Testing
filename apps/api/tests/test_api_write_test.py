"""`write_test` items (SPEC 5.2 / 5.7): trusted client verdict, diagnostic-only."""

from __future__ import annotations

from datetime import timedelta

import pytest
import yaml

from app.models import tables as t
from app.services import scoring as sc

SID = "py.a.three"  # fixture subtopic whose only level-2 item we replace with a write_test
WT = {
    "id": "WT1",
    "type": "write_test",
    "minutes": 8,
    "difficulty": 2,
    "prompt_md": "write a test",
    "problem_id": "write-test-add",
    "practices": ["verify"],
}


@pytest.fixture
def wt_client(content_dir, make_client):
    """An app whose py.a.three has one level-2 write_test item and its problem dir."""
    pdir = content_dir / "problems" / SID / "write-test-add"
    pdir.mkdir(parents=True)
    (pdir / "problem.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "write-test-add",
                "subtopic_id": SID,
                "kind": "check",
                "item_kind": "write_test",
                "title": "Write a test: add",
                "title_vi": "Viết test",
                "source": {"type": "original"},
                "statement_en_md": "spec",
                "statement_vi_md": "spec vi",
                "starter": {"python": "def test_x():\n    ...\n"},
                "status": "validated",
                "version": 1,
            },
            allow_unicode=True,
        )
    )
    (pdir / "buggy.py").write_text("def add(a, b):\n    return a - b\n")
    (pdir / "solution.py").write_text("def add(a, b):\n    return a + b\n")
    (content_dir / "checks" / f"{SID}.yaml").write_text(
        yaml.safe_dump({"subtopic_id": SID, "items": [WT]})
    )
    return make_client()


def start(c):
    return c.post(f"/api/checks/{SID}/start")


def body(session, ok=True, **kw):
    return {
        "session_id": session,
        "item_id": "WT1",
        "elapsed_ms": 60_000,
        "code": "def test_add():\n    assert add(1, 2) == 3\n",
        "language": "python",
        "verdict": "AC" if ok else "WA",
        "passed_tests": 2 if ok else 1,
        "total": 2,
        **kw,
    }


def answer(c, b):
    return c.post(f"/api/checks/{SID}/answer", json=b)


def map_row(c):
    return next(s for s in c.get("/api/map").json()["subtopics"] if s["id"] == SID)


def test_start_serves_the_write_test_item_with_its_problem_id(wt_client):
    step = start(wt_client).json()["step"]
    assert (step["item_id"], step["type"], step["problem_id"]) == (
        "WT1",
        "write_test",
        "write-test-add",
    )
    assert "buggy" not in str(step)


def test_get_problem_carries_the_write_test_fields(wt_client):
    p = wt_client.get("/api/problems/write-test-add").json()
    assert p["item_kind"] == "write_test"
    assert p["buggy_code"] == "def add(a, b):\n    return a - b\n"
    assert p["reference_code"] == "def add(a, b):\n    return a + b\n"
    assert p["starter_test"] == "def test_x():\n    ...\n"
    assert p["statement_en_md"] == "spec" and p["statement_vi_md"] == "spec vi"
    # a normal problem's response is unchanged
    normal = wt_client.get("/api/problems/add-two").json()
    assert not {"item_kind", "buggy_code", "reference_code", "starter_test"} & normal.keys()


def test_grade_trusts_the_client_verdict_and_records_a_write_test_attempt(wt_client):
    sess = start(wt_client).json()["session_id"]
    r = answer(wt_client, body(sess)).json()
    assert r["result"]["correct"] and r["result"]["clean"] and r["result"]["type"] == "write_test"
    assert (r["result"]["tests_passed"], r["result"]["tests_total"]) == (2, 2)
    with wt_client.app.state.rt.session() as db:
        cr = db.query(t.CheckResult).one()
        assert (cr.item_type, cr.passed, cr.clean) == ("write_test", True, True)
        att = db.query(t.Attempt).one()
        assert (att.problem_id, att.verdict, att.passed, att.total) == (
            "write-test-add",
            "AC",
            2,
            2,
        )


@pytest.mark.parametrize(
    ("patch", "code"),
    [
        ({"code": None}, "missing_field"),
        ({"verdict": None}, "missing_field"),
        ({"passed_tests": None}, "missing_field"),
        ({"total": None}, "missing_field"),
        ({"passed_tests": 3}, "invalid_counts"),  # passed_tests > total
        ({"verdict": "AC", "passed_tests": 1}, "invalid_counts"),  # AC needs passed == total
    ],
)
def test_grade_internal_consistency_is_422(wt_client, patch, code):
    sess = start(wt_client).json()["session_id"]
    r = answer(wt_client, body(sess) | patch)
    assert r.status_code == 422 and r.json()["error"]["code"] == code


def test_wrong_write_test_never_locks_and_never_changes_score_or_lock_reasons(wt_client):
    before = map_row(wt_client)
    sess = start(wt_client).json()["session_id"]
    r = answer(wt_client, body(sess, ok=False)).json()
    assert r["result"]["correct"] is False and r["result"]["reason"] == "wrong_answer"
    assert r["finished"] and r["outcome"]["retry_after"] is None
    assert r["score"]["before"] == r["score"]["after"] == 0
    after = map_row(wt_client)
    assert after["score"] == before["score"] == 0
    assert after["lock_reasons"] == before["lock_reasons"]
    assert (after["unlocked"], after["tested_out"]) == (before["unlocked"], before["tested_out"])
    # no 24 h lock: a new attempt starts straight away
    again = start(wt_client)
    assert again.status_code == 200, again.text


def test_clean_write_test_does_not_raise_the_score(wt_client):
    sess = start(wt_client).json()["session_id"]
    r = answer(wt_client, body(sess)).json()
    assert r["result"]["clean"] is True
    assert r["finished"] and r["outcome"]["level3"] is None  # does not climb to level 3
    assert r["score"]["after"] == 0 and r["score"]["tested_out"] is False
    row = map_row(wt_client)
    assert (row["score"], row["tested_out"]) == (0, False)
    # the level is not "passed": a fresh check can start again
    assert start(wt_client).status_code == 200


# ---- scoring: pure function ----


def _ev(*checks, **kw):
    return sc.Evidence(checks=checks, **kw)


def test_scoring_ignores_write_test_everywhere():
    spec = sc.SubtopicSpec(has_l2_items=True, has_l3_write_code=False, is_concept=False)
    clean2 = sc.CheckEv("WT1", 2, True, True, item_type="write_test")
    assert sc.score(spec, _ev(clean2)).score == 0
    assert not sc.score(spec, _ev(clean2)).tested_out
    clean1 = sc.CheckEv("WT1", 1, True, True, item_type="write_test", context="placement")
    assert not sc.score(spec, _ev(clean1)).tested_basic
    # a failed write_test at level 2 must not open the fail-then-practice exit
    quiz = tuple(sc.QuizAnswerEv(f"d#q{i}", 1, 1, True) for i in range(3))
    base = {
        "lesson_done": True,
        "quiz_answers": quiz,
        "attempts": (sc.AttemptEv("p1", True, True),),
    }
    spec2 = sc.SubtopicSpec(
        practice_ids=("p1",), has_l2_items=True, graded_quiz_ids=("d#q0", "d#q1", "d#q2")
    )
    failed_wt = sc.CheckEv("WT1", 2, False, False, item_type="write_test")
    failed_wc = sc.CheckEv("Q1", 2, False, False, item_type="write_code")
    assert sc.score(spec2, _ev(failed_wt, **base)).score == 1
    assert sc.score(spec2, _ev(failed_wc, **base)).score == 2  # the control: write_code opens it


# ---- in-flow: the write_test closes a mastery ladder as a last diagnostic step ----

ONE = "py.a.one"  # Q1 concept (L1), Q2 write_code (L2), Q3 write_code (L3)
WT_ONE = {**WT, "id": "F9", "problem_id": "check-q2"}


@pytest.fixture
def flow_client(content_dir, make_client):
    path = content_dir / "checks" / f"{ONE}.yaml"
    data = yaml.safe_load(path.read_text())
    data["items"].append(WT_ONE)
    path.write_text(yaml.safe_dump(data))
    return make_client()


def _code(session, item, ok):
    return {
        "session_id": session,
        "item_id": item,
        "elapsed_ms": 60_000,
        "code": "x = 1\n",
        "verdict": "AC" if ok else "WA",
        "passed_tests": 2 if ok else 0,
        "total": 2,
    }


def _post(c, b):
    return c.post(f"/api/checks/{ONE}/answer", json=b).json()


def _results(c):
    with c.app.state.rt.session() as db:
        return [(r.item_id, r.level, r.passed, r.item_type) for r in db.query(t.CheckResult)]


def test_write_test_closes_the_pass_path_once_and_changes_nothing(flow_client):
    sid = flow_client.post(f"/api/checks/{ONE}/start").json()["session_id"]
    r = _post(flow_client, _code(sid, "Q2", True))
    assert r["next"]["item_id"] == "Q3" and r["next"]["level"] == 3
    r = _post(flow_client, _code(sid, "Q3", True))
    # the scoring ladder ended, but the session stays open on the diagnostic write_test
    assert not r["finished"] and r["status"] == "in_progress" and r["outcome"] is None
    assert (r["next"]["item_id"], r["next"]["type"], r["next"]["index"]) == ("F9", "write_test", 2)
    assert r["next"]["problem_id"] == "check-q2" and r["next"]["count"] == 3
    score_before = r["score"]["after"]
    view = flow_client.post(f"/api/checks/{ONE}/start").json()  # resume shows the same step
    assert view["resumed"] and view["step"]["item_id"] == "F9"

    fin = _post(flow_client, _code(sid, "F9", False))  # non-AC: still no lock, no score change
    assert fin["finished"] and fin["next"] is None
    assert fin["score"]["before"] == fin["score"]["after"] == score_before
    out = fin["outcome"]
    assert (out["level2"], out["level3"], out["level1"]) == ("passed", "passed", None)
    assert out["retry_after"] is None
    assert [x[3] for x in _results(flow_client)] == ["write_code", "write_code", "write_test"]
    again = _post(flow_client, _code(sid, "F9", True))
    assert again["error"]["code"] == "check_session_done"  # served exactly once


def test_write_test_closes_the_fail_path_and_keeps_the_l2_lock(flow_client):
    sid = flow_client.post(f"/api/checks/{ONE}/start").json()["session_id"]
    r = _post(flow_client, _code(sid, "Q2", False))
    assert r["next"]["item_id"] == "Q1" and r["next"]["level"] == 1  # scoring fall, as before
    r = _post(flow_client, {"session_id": sid, "item_id": "Q1", "self_grade": True})
    assert not r["finished"] and r["next"]["type"] == "write_test"
    fin = _post(flow_client, _code(sid, "F9", True))  # a clean AC write_test ...
    assert fin["finished"] and fin["result"]["clean"] is True
    out = fin["outcome"]
    # ... neither overwrites the real L2 label nor removes / moves the lock of the failed L2
    assert (out["level1"], out["level2"], out["level3"]) == ("passed", "failed", None)
    assert fin["score"]["after"] == 0 and out["tested_out"] is False
    with flow_client.app.state.rt.session() as db:
        q2 = next(x for x in db.query(t.CheckResult) if x.item_id == "Q2")
        lock = (q2.taken_at + timedelta(hours=24)).isoformat()
    assert out["retry_after"] == lock
    locked = flow_client.post(f"/api/checks/{ONE}/start")
    assert locked.status_code == 409
    assert locked.json()["error"]["code"] == "check_retry_locked"
    assert locked.json()["error"]["retry_after"] == lock


def test_first_write_test_skips_the_ones_already_shown(flow_client):
    from app.services import checks

    content = flow_client.app.state.rt.content
    assert checks._first_write_test(content, ONE, set())["id"] == "F9"
    assert checks._first_write_test(content, ONE, {"F9"}) is None
