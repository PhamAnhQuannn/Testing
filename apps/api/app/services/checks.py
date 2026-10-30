"""Mastery check and test out: the ladder, grading and persistence (SPEC 2.3 flows C and D, 5.2).

Results go to `check_results` (append-only evidence); the score is never set here, it is recomputed
by `progress.recompute_subtopic` -> `scoring.score` after each result.

Ladder: level 2 first (write_code preferred). A correct answer goes on to level 3 (if the subtopic
has one), clean or not; a wrong answer or "give up" goes down to level 1 as a diagnostic (no level
1 item: stop, "learn the lesson"). Only a wrong (not given-up) answer starts the 24 h lock. `clean`
(no solution, <= 1 hint, in time) alone gates score-2/3 evidence. Level 1 never changes the score.
A subtopic whose level 2 is already (clean) passed starts at level 3. `concept` items are
self-graded: on a code subtopic they are recorded but never `clean`, so they are never evidence
for score 2 or 3; on a concept subtopic (System Design + the AI-engineer LLM track, no code to
measure) a correct in-time self-graded pass is `clean` and is the approved score-2/3 evidence.
"""

from __future__ import annotations

import copy
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..errors import ApiError
from ..models import tables as t
from . import progress
from .content_loader import ContentStore

LOCK = timedelta(hours=24)  # redo lock after a failed level (SPEC flow C step 4)
SESSION_TTL = timedelta(hours=24)  # no activity this long: the session expires (not a failure)
CLEAN_TIME_FACTOR = 1.5  # SPEC 5.1 `clean`
CONTEXTS = ("mastery", "test_out")

_TYPE_ORDER = {
    2: {"write_code": 0, "read_code": 1, "concept": 2},
    3: {"write_code": 0, "read_code": 1, "concept": 2},
    1: {"read_code": 0, "concept": 1, "write_code": 2},  # diagnostic: lightest first
}


# ---- ladder helpers ----


def find_item(content: ContentStore, subtopic_id: str, item_id: str) -> dict[str, Any] | None:
    """Mastery pool first, then the placement-only pool (mcq / read_code rungs)."""
    return content.find_check_item(subtopic_id, item_id)


def pick_item(
    content: ContentStore, subtopic_id: str, level: int, attempt_no: int
) -> dict[str, Any] | None:
    """Best-typed item of a level, drawn from the lesson's curated `mastery_check` items when it
    names any (else all items of the level); with several of the same type a redo rotates."""
    items = content.curated_check_items(subtopic_id)[level]
    if not items:
        return None
    order = _TYPE_ORDER[level]
    best = min(order.get(i["type"], 9) for i in items)
    group = [i for i in items if order.get(i["type"], 9) == best]
    return group[(max(attempt_no, 1) - 1) % len(group)]


def _step(item: dict[str, Any], level: int) -> dict[str, Any]:
    return {
        "item_id": item["id"],
        "level": level,
        "type": item["type"],
        "minutes": item.get("minutes") or 10,
        "result": None,
    }


def level_passed(db: Session, user_id: int, subtopic_id: str, level: int) -> bool:
    """A clean pass of this level that counts as evidence.

    On a code subtopic a self-graded concept is never clean, so it never qualifies here; on a
    concept subtopic a clean self-graded concept pass does (level 3 still narrows to write_code,
    which concept subtopics lack, so their level-3 ladder stays re-attemptable — scoring reads
    `check_results` directly and is unaffected).
    """
    q = select(t.CheckResult.id).where(
        t.CheckResult.user_id == user_id,
        t.CheckResult.subtopic_id == subtopic_id,
        t.CheckResult.level == level,
        t.CheckResult.passed.is_(True),
        t.CheckResult.clean.is_(True),
    )
    if level == 3:
        q = q.where(t.CheckResult.item_type == "write_code")
    return db.scalar(q.limit(1)) is not None


def retry_after(
    db: Session, user_id: int, subtopic_id: str, level: int, now: datetime
) -> datetime | None:
    """End of the 24 h lock after the last failed (not given-up) result of this level."""
    last = db.scalar(
        select(func.max(t.CheckResult.taken_at)).where(
            t.CheckResult.user_id == user_id,
            t.CheckResult.subtopic_id == subtopic_id,
            t.CheckResult.level == level,
            t.CheckResult.passed.is_(False),
            t.CheckResult.gave_up.is_(False),
        )
    )
    if last is None:
        return None
    until = last + LOCK
    return until if until > now else None


def _expires_at(sess: t.CheckSession) -> datetime:
    return sess.last_active_at + SESSION_TTL


def _current_step(ladder: dict[str, Any]) -> dict[str, Any] | None:
    return next((s for s in ladder["steps"] if s["result"] is None), None)


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() if moment else None


# ---- public shapes (never contain reference / expected output) ----


def public_item(content: ContentStore, subtopic_id: str, step: dict[str, Any]) -> dict[str, Any]:
    item = find_item(content, subtopic_id, step["item_id"]) or {}
    out: dict[str, Any] = {
        "item_id": step["item_id"],
        "level": step["level"],
        "type": step["type"],
        "minutes": step["minutes"],
        "time_limit_ms": int(step["minutes"] * 60_000),
        "prompt_md": item.get("prompt_md", ""),
    }
    if step["type"] == "write_code":
        out["problem_id"] = item.get("problem_id")
    elif step["type"] == "read_code":
        out["code"] = item.get("code", "")
    elif step["type"] == "mcq":
        out["choices"] = list(item.get("choices", []))  # never answer_index / explanation
    elif step["type"] == "concept":
        out["answer_md"] = item.get("answer_md", "")  # self-graded: shown after the attempt
    return out


def _results(ladder: dict[str, Any]) -> list[dict[str, Any]]:
    return [{**s["result"], "item_id": s["item_id"], "level": s["level"]} for s in ladder["steps"]
            if s["result"] is not None]  # fmt: skip


def session_view(
    content: ContentStore, sess: t.CheckSession, *, resumed: bool = False
) -> dict[str, Any]:
    step = _current_step(sess.ladder)
    return {
        "session_id": sess.id,
        "subtopic_id": sess.subtopic_id,
        "context": sess.context,
        "attempt_no": sess.attempt_no,
        "status": sess.status,
        "resumed": resumed,
        "elapsed_ms": sess.elapsed_ms,
        "started_at": _iso(sess.started_at),
        "expires_at": _iso(_expires_at(sess)),
        "step": (
            {
                "index": sess.ladder["steps"].index(step),
                "count": len(sess.ladder["steps"]),
                **public_item(content, sess.subtopic_id, step),
            }
            if step
            else None
        ),
        "results": _results(sess.ladder),
    }


# ---- start ----


def start(
    db: Session,
    content: ContentStore,
    user_id: int,
    subtopic_id: str,
    context: str,
    now: datetime,
    *,
    key: str | None = None,
) -> tuple[t.CheckSession, bool]:
    """Begin a check, or resume the in-progress one (< 24 h idle). Returns (session, resumed)."""
    if subtopic_id not in content.subtopics:
        raise ApiError(404, "subtopic_not_found", f"Unknown subtopic {subtopic_id}")
    if not content.check_items(subtopic_id)[2]:
        raise ApiError(404, "check_not_found", f"No level-2 check item for {subtopic_id}")

    sess = db.scalar(
        select(t.CheckSession)
        .where(
            t.CheckSession.user_id == user_id,
            t.CheckSession.subtopic_id == subtopic_id,
            t.CheckSession.status == "in_progress",
            t.CheckSession.context != "placement",  # a placement gate is resumed by placement
        )
        .order_by(t.CheckSession.id.desc())
        .limit(1)
    )
    if sess is not None:
        if now >= _expires_at(sess):
            sess.status = "expired"  # not a failure; results already given stay as evidence
            db.flush()
        else:
            sess.last_active_at = now
            db.flush()
            return sess, True

    level = 3 if level_passed(db, user_id, subtopic_id, 2) else 2
    # The level-3 gate is a write_code item, or on a concept subtopic (no code) any level-3 item.
    l3_items = content.check_items(subtopic_id)[3]
    has_l3_gate = any(i["type"] == "write_code" for i in l3_items) or (
        content.spec_for(subtopic_id).is_concept and bool(l3_items)
    )
    if level == 3 and (not has_l3_gate or level_passed(db, user_id, subtopic_id, 3)):
        raise ApiError(409, "check_already_passed", "Nothing left to check for this subtopic")
    until = retry_after(db, user_id, subtopic_id, level, now)
    if until is not None:
        raise ApiError(
            409,
            "check_retry_locked",
            f"Level {level} can be retried after {until.isoformat()}",
            retry_after=until.isoformat(),
            level=level,
        )

    return begin_session(db, content, user_id, subtopic_id, context, level, now, key=key), False


def begin_session(
    db: Session,
    content: ContentStore,
    user_id: int,
    subtopic_id: str,
    context: str,
    level: int,
    now: datetime,
    *,
    key: str | None = None,
    item: dict[str, Any] | None = None,
    placement_session_id: int | None = None,
) -> t.CheckSession:
    """Open a new session at `level` (best item, or the given `item`); the caller has already
    checked the lock. Placement (SPEC 5.6) opens one per gate with its own item."""
    prev = db.scalar(
        select(func.max(t.CheckResult.attempt_no)).where(
            t.CheckResult.user_id == user_id, t.CheckResult.subtopic_id == subtopic_id
        )
    )
    attempt_no = (prev or 0) + 1
    if item is None:
        item = pick_item(content, subtopic_id, level, attempt_no)
    assert item is not None
    # a new attempt starts with a clean slate of hints / solution views on its code items
    for it in content.checks.get(subtopic_id, []):
        pid = it.get("problem_id")
        st = db.get(t.ProblemState, (user_id, pid)) if pid else None
        if st is not None:
            st.hints_used = 0
            st.solution_viewed = False
            st.first_opened_at = None

    sess = t.CheckSession(
        user_id=user_id,
        subtopic_id=subtopic_id,
        context=context,
        placement_session_id=placement_session_id,
        order_no=0,
        attempt_no=attempt_no,
        status="in_progress",
        ladder={"steps": [_step(item, level)]},
        current_item_id=item["id"],
        elapsed_ms=0,
        started_at=now,
        last_active_at=now,
    )
    db.add(sess)
    db.flush()
    progress.record_event(
        db,
        "check_started",
        {
            "session_id": sess.id,
            "subtopic_id": subtopic_id,
            "context": context,
            "attempt_no": attempt_no,
            "level": level,
        },
        now=now,
        idem_key=key,
    )
    return sess


# ---- answer ----


def _norm(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def _grade(
    db: Session,
    content: ContentStore,
    user_id: int,
    sess: t.CheckSession,
    step: dict[str, Any],
    body: Any,
    now: datetime,
    key: str | None,
) -> dict[str, Any]:
    """Grade one item. Returns {correct, passed, clean, gave_up, reason?, ...} (no reference)."""
    item = find_item(content, sess.subtopic_id, step["item_id"]) or {}
    limit_ms = CLEAN_TIME_FACTOR * step["minutes"] * 60_000
    in_time = body.elapsed_ms <= limit_ms
    if body.gave_up:
        return {"correct": False, "passed": False, "clean": False, "gave_up": True}

    kind = step["type"]
    if kind == "concept":
        if body.self_grade is None:
            raise ApiError(422, "missing_field", "self_grade is required for a concept item")
        passed = bool(body.self_grade)
        # On a concept subtopic (System Design + the AI-engineer LLM track, SPEC 5.2) there is no
        # code to measure, so a correct, in-time self-graded concept pass IS the approved evidence
        # for score 2/3. On every other subtopic a self-graded concept is recorded but never clean,
        # so it can never be evidence (the score-2 bar still rests on measured code there).
        is_concept = content.spec_for(sess.subtopic_id).is_concept
        clean = passed and in_time if is_concept else False
        return {
            "correct": passed,
            "passed": passed,
            "clean": clean,
            "gave_up": False,
            "counts_as_evidence": is_concept and clean,
        }

    if kind == "mcq":
        choice = getattr(body, "choice", None)
        if choice is None:
            raise ApiError(422, "missing_field", "choice is required for an mcq item")
        correct = choice == item.get("answer_index")
        clean = correct and in_time
        res = {"correct": correct, "passed": correct, "clean": clean, "gave_up": False}
        if not correct:
            res["reason"] = "wrong_answer"
        elif not clean:
            res["reason"] = "over_time"
        return res

    if kind == "read_code":
        if body.answer is None:
            raise ApiError(422, "missing_field", "answer is required for a read_code item")
        correct = _norm(body.answer) == _norm(str(item.get("expected_output", "")))
        clean = correct and in_time
        res = {"correct": correct, "passed": correct, "clean": clean, "gave_up": False}
        if not correct:
            res["reason"] = "wrong_answer"
        elif not clean:
            res["reason"] = "over_time"
        return res

    # write_code: the browser ran the hidden tests (same engine as Submit); we record an attempt
    if body.code is None or body.verdict is None or body.passed_tests is None or body.total is None:
        raise ApiError(
            422, "missing_field", "code, verdict, passed_tests and total are required here"
        )
    if body.passed_tests > body.total:
        raise ApiError(422, "invalid_counts", "passed_tests cannot exceed total")
    ac = body.verdict == "AC"
    if ac and body.passed_tests != body.total:
        raise ApiError(422, "invalid_counts", "an AC verdict needs passed_tests == total")
    pid = item.get("problem_id")
    problem = content.check_problem(pid) if pid else None
    if problem is None:
        raise ApiError(404, "problem_not_found", f"No check problem for item {step['item_id']}")
    st = db.get(t.ProblemState, (user_id, pid))
    hints = st.hints_used if st and st.hints_used else 0
    viewed = bool(st and st.solution_viewed)
    clean = ac and not viewed and hints <= 1 and in_time
    db.add(
        t.Attempt(
            user_id=user_id,
            problem_id=pid,
            mode="submit",
            language=body.language,
            code=body.code,
            verdict=body.verdict,
            passed=body.passed_tests,
            total=body.total,
            elapsed_ms=body.elapsed_ms,
            runtime_ms=body.runtime_ms,
            hints_used=hints,
            solution_viewed=viewed,
            clean=clean,
            started_at=st.first_opened_at if st else None,
            submitted_at=now,
            problem_version=content.problem_version(db, pid),
        )
    )
    progress.record_event(
        db,
        "attempt",
        {
            "problem_id": pid,
            "mode": "submit",
            "verdict": body.verdict,
            "passed": body.passed_tests,
            "total": body.total,
            "elapsed_ms": body.elapsed_ms,
            "clean": clean,
            "check_session_id": sess.id,
        },
        now=now,
        idem_key=key,
    )
    res = {
        "correct": ac,
        "passed": ac,  # ladder/lock key on correctness; `clean` alone gates score-2/3 evidence
        "clean": clean,
        "gave_up": False,
        "verdict": body.verdict,
        "tests_passed": body.passed_tests,
        "tests_total": body.total,
    }
    if ac and not clean:
        res["reason"] = "solution_viewed" if viewed else "hint_limit" if hints > 1 else "over_time"
    elif not ac:
        res["reason"] = "wrong_answer"
    return res


def _advance(
    content: ContentStore, sess: t.CheckSession, ladder: dict[str, Any], step: dict[str, Any]
) -> None:
    """Add the next step after `step` was answered, or mark the session done."""
    res = step["result"]
    nxt_level = None
    if step["level"] == 2 and sess.context != "placement":
        # placement drives its own P0/P1/P2 rungs (SPEC 5.6): a level-2 answer there always ends
        # the session (no level-3, no auto level-1 diagnostic)
        nxt_level = 3 if res["correct"] else 1
    if nxt_level is not None:
        item = pick_item(content, sess.subtopic_id, nxt_level, sess.attempt_no)
        if item is not None:
            ladder["steps"].append(_step(item, nxt_level))
            sess.current_item_id = item["id"]
            return
        ladder["need_lesson"] = nxt_level == 1  # no level 1 item: "learn the lesson first"
    sess.current_item_id = None
    sess.status = "done"


def answer(
    db: Session,
    content: ContentStore,
    user_id: int,
    subtopic_id: str,
    body: Any,
    now: datetime,
    *,
    key: str | None = None,
) -> dict[str, Any]:
    sess = db.get(t.CheckSession, body.session_id)
    if sess is None or sess.user_id != user_id or sess.subtopic_id != subtopic_id:
        raise ApiError(404, "check_session_not_found", f"No check session {body.session_id}")
    if sess.status == "expired" or (sess.status == "in_progress" and now >= _expires_at(sess)):
        raise ApiError(409, "check_session_expired", "This check expired; start a new one")
    if sess.status != "in_progress":
        raise ApiError(409, "check_session_done", "This check is already finished")
    ladder = copy.deepcopy(sess.ladder)
    step = _current_step(ladder)
    assert step is not None
    if body.item_id != step["item_id"]:
        raise ApiError(
            409, "check_wrong_item", f"The current item is {step['item_id']}, not {body.item_id}"
        )

    res = _grade(db, content, user_id, sess, step, body, now, key)
    prev = db.scalar(
        select(t.CheckResult.id).where(
            t.CheckResult.user_id == user_id,
            t.CheckResult.session_id == sess.id,
            t.CheckResult.item_id == step["item_id"],
        )
    )
    if prev is not None:  # defensive: one result per item per session
        raise ApiError(409, "check_item_answered", "This item was already answered")
    db.add(
        t.CheckResult(
            user_id=user_id,
            subtopic_id=subtopic_id,
            item_id=step["item_id"],
            level=step["level"],
            attempt_no=sess.attempt_no,
            passed=res["passed"],
            clean=res["clean"],
            minutes_used=body.elapsed_ms / 60_000,
            taken_at=now,
            session_id=sess.id,
            context=sess.context,
            gave_up=res["gave_up"],
            item_type=step["type"],
        )
    )
    progress.record_event(
        db,
        "check_item_result",
        {
            "session_id": sess.id,
            "subtopic_id": subtopic_id,
            "item_id": step["item_id"],
            "level": step["level"],
            "attempt_no": sess.attempt_no,
            "passed": res["passed"],
            "clean": res["clean"],
            "gave_up": res["gave_up"],
            "context": sess.context,
        },
        now=now,
        idem_key=key,
    )
    step["result"] = {k: v for k, v in res.items() if k != "counts_as_evidence"} | {
        "at": now.isoformat()
    }
    sess.elapsed_ms = max(sess.elapsed_ms or 0, body.session_elapsed_ms or 0)
    sess.last_active_at = now
    _advance(content, sess, ladder, step)
    sess.ladder = ladder  # reassign: SQLAlchemy does not track in-place JSON changes
    db.flush()

    info = progress.recompute_subtopic(db, content, subtopic_id, now, event_time=now)
    row = db.get(t.UserSubtopic, (user_id, subtopic_id))
    out: dict[str, Any] = {
        "session_id": sess.id,
        "status": sess.status,
        "finished": sess.status == "done",
        "result": {
            "item_id": step["item_id"],
            "level": step["level"],
            "type": step["type"],
            **{k: v for k, v in res.items()},
        },
        "next": None,
        "score": {
            "subtopic_id": subtopic_id,
            "before": info["before"],
            "after": info["after"],
            "status": row.status if row else None,
            "tested_out": bool(row and row.tested_out),
            "newly_unlocked": info["newly_unlocked"],
        },
        "outcome": None,
    }
    if sess.status == "in_progress":
        nxt = _current_step(ladder)
        assert nxt is not None
        out["next"] = {
            "index": ladder["steps"].index(nxt),
            "count": len(ladder["steps"]),
            **public_item(content, subtopic_id, nxt),
        }
    else:
        out["outcome"] = _outcome(sess, ladder, row, info)
    return out


def _outcome(
    sess: t.CheckSession, ladder: dict[str, Any], row: t.UserSubtopic | None, info: dict[str, Any]
) -> dict[str, Any]:
    by_level: dict[int, dict[str, Any]] = {}
    for s in ladder["steps"]:
        if s["result"] is not None:
            by_level[s["level"]] = s["result"]

    def label(level: int) -> str | None:
        r = by_level.get(level)
        if r is None:
            return None
        return "gave_up" if r["gave_up"] else "passed" if r["passed"] else "failed"

    lock_until: str | None = None
    for level in (2, 3):
        r = by_level.get(level)
        if r is not None and not r["passed"] and not r["gave_up"]:
            lock_until = _iso(datetime.fromisoformat(r["at"]) + LOCK)
    return {
        "level1": label(1),
        "level2": label(2),
        "level3": label(3),
        "tested_out": bool(row and row.tested_out),
        "score": info["after"],
        "need_lesson": bool(ladder.get("need_lesson")),
        "retry_after": lock_until,
        "newly_unlocked": info["newly_unlocked"],
    }


# ---- heartbeat ----


def heartbeat(
    db: Session, user_id: int, session_id: int, elapsed_ms: int, now: datetime
) -> t.CheckSession:
    sess = db.get(t.CheckSession, session_id)
    if sess is None or sess.user_id != user_id:
        raise ApiError(404, "check_session_not_found", f"No check session {session_id}")
    if sess.status == "expired" or (sess.status == "in_progress" and now >= _expires_at(sess)):
        raise ApiError(409, "check_session_expired", "This check expired; start a new one")
    if sess.status == "in_progress":
        sess.elapsed_ms = max(sess.elapsed_ms or 0, elapsed_ms)  # absolute: safe to resend
        sess.last_active_at = now
    db.flush()
    return sess


def expires_iso(sess: t.CheckSession) -> str | None:
    return _iso(_expires_at(sess))
