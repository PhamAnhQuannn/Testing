"""Lesson runs, quiz answers, lesson_done."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import func, select

from ..deps import DB, Content, IdemKey, Now, User
from ..errors import ApiError
from ..models import tables as t
from ..services import progress
from .content import current_run

router = APIRouter(prefix="/api")


def _norm_output(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def grade(block: dict[str, Any], answer: Any) -> tuple[bool, Any]:
    """Returns (correct, correct_answer_to_reveal)."""
    kind = block["type"]
    if kind == "quiz_mcq":
        want = set(block["answer"])
        if not isinstance(answer, list):
            raise ApiError(422, "invalid_answer", "quiz_mcq answer must be a list of option ids")
        return set(answer) == want, list(block["answer"])
    if kind == "quiz_fill":
        blanks = block["blanks"]
        if not isinstance(answer, list) or len(answer) != len(blanks):
            raise ApiError(422, "invalid_answer", f"quiz_fill needs {len(blanks)} answers")
        ok = True
        for given, b in zip(answer, blanks, strict=True):
            given = str(given).strip()
            good = given in b["accept"]
            if not good and b.get("regex"):
                good = re.fullmatch(b["regex"], given) is not None
            ok = ok and good
        return ok, [b["accept"][0] for b in blanks]
    if kind == "predict_output":
        if not isinstance(answer, str):
            raise ApiError(422, "invalid_answer", "predict_output answer must be a string")
        return _norm_output(answer) == _norm_output(block["expected_output"]), block[
            "expected_output"
        ]
    raise ApiError(422, "not_a_quiz", f"Block {block['id']} is not gradable")


class RunOut(BaseModel):
    run_no: int


@router.post("/lessons/{subtopic_id}/runs", status_code=201)
def new_run(subtopic_id: str, db: DB, user: User, content: Content, now: Now, key: IdemKey):
    if content.lesson(subtopic_id) is None:
        raise ApiError(404, "lesson_not_found", f"No lesson for {subtopic_id}")
    cur = current_run(db, user.id, subtopic_id)
    if db.get(t.LessonRun, (user.id, subtopic_id, 1)) is None:
        db.add(t.LessonRun(user_id=user.id, subtopic_id=subtopic_id, run_no=1, started_at=now))
    run_no = cur + 1
    db.add(t.LessonRun(user_id=user.id, subtopic_id=subtopic_id, run_no=run_no, started_at=now))
    progress.record_event(
        db, "lesson_run", {"subtopic_id": subtopic_id, "run_no": run_no}, now=now, idem_key=key
    )
    db.commit()
    return {"run_no": run_no}


class QuizAnswerIn(BaseModel):
    quiz_item_id: str  # "<subtopic_id>#<block_id>"
    run_no: int = 1
    answer: Any
    occurred_at: datetime | None = None


@router.post("/quiz/answers")
def post_quiz_answer(
    body: QuizAnswerIn, db: DB, user: User, content: Content, now: Now, key: IdemKey
):
    if "#" not in body.quiz_item_id:
        raise ApiError(422, "invalid_quiz_item", "quiz_item_id must be '<subtopic>#<block>'")
    sid, block_id = body.quiz_item_id.split("#", 1)
    lesson = content.lesson(sid)
    block = lesson.block(block_id) if lesson else None
    if lesson is None or block is None:
        raise ApiError(404, "quiz_item_not_found", f"Unknown quiz item {body.quiz_item_id}")
    cur = current_run(db, user.id, sid)
    if body.run_no < 1 or body.run_no > cur:
        raise ApiError(422, "invalid_run", f"run_no must be in 1..{cur}")
    correct, reveal = grade(block, body.answer)
    prev = db.scalar(
        select(func.count())
        .select_from(t.QuizAnswer)
        .where(
            t.QuizAnswer.user_id == user.id,
            t.QuizAnswer.quiz_item_id == body.quiz_item_id,
            t.QuizAnswer.run_no == body.run_no,
        )
    )
    attempt_no = (prev or 0) + 1
    occurred = progress.clamp_occurred(body.occurred_at, now)
    db.add(
        t.QuizAnswer(
            user_id=user.id,
            quiz_item_id=body.quiz_item_id,
            run_no=body.run_no,
            attempt_no=attempt_no,
            answer=body.answer,
            correct=correct,
            answered_at=occurred,
        )
    )
    progress.record_event(
        db,
        "quiz_answer",
        {
            "quiz_item_id": body.quiz_item_id,
            "run_no": body.run_no,
            "attempt_no": attempt_no,
            "correct": correct,
        },
        now=now,
        occurred_at=body.occurred_at,
        idem_key=key,
    )
    db.flush()
    graded = block["type"] in {"quiz_mcq", "quiz_fill", "predict_output"} and block.get(
        "graded", True
    )
    # a quiz passed after lesson_done lifts the score without a second /complete
    progress.recompute_subtopic(db, content, sid, now, event_time=occurred)
    best = db.get(t.UserSubtopic, (user.id, sid)).quiz_best
    db.commit()
    return {
        "correct": correct,
        "attempt_no": attempt_no,
        "run_no": body.run_no,
        "first_attempt": attempt_no == 1,
        "graded": graded,
        "explain_md": block.get("explain_md"),
        "correct_answer": reveal,
        "quiz_best": best,
    }


class CompleteIn(BaseModel):
    occurred_at: datetime | None = None


@router.post("/lessons/{subtopic_id}/complete")
def complete_lesson(
    subtopic_id: str,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
    body: CompleteIn | None = None,
):
    if content.lesson(subtopic_id) is None:
        raise ApiError(404, "lesson_not_found", f"No lesson for {subtopic_id}")
    occurred = progress.clamp_occurred(body.occurred_at if body else None, now)
    row = db.get(t.UserSubtopic, (user.id, subtopic_id))
    assert row is not None
    if row.lesson_done_at is None:
        progress.record_event(
            db,
            "lesson_done",
            {"subtopic_id": subtopic_id},
            now=now,
            occurred_at=occurred,
            idem_key=key,
        )
    # always recompute: a repeat call after a late quiz answer still refreshes caches
    info = progress.recompute_subtopic(db, content, subtopic_id, now, event_time=occurred)
    res = progress.compute_score(db, content, subtopic_id, user.id)
    card = db.get(t.ReviewCard, (user.id, subtopic_id))
    db.commit()
    return {
        "subtopic_id": subtopic_id,
        "lesson_done": True,
        "quiz_best": res.quiz_best,
        "quiz_passed": res.s1,
        "score": res.score,
        "score_before": info["before"],
        "status": row.status,
        "review_card": {"box": card.box, "due_on": card.due_on.isoformat()} if card else None,
        "newly_unlocked": info["newly_unlocked"],
    }
