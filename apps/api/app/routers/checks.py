"""Mastery check (flow C) and test out (flow D). Paths follow SPEC 6.4; see docs/API_M2A.md."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..deps import DB, Content, IdemKey, Now, User
from ..services import checks

router = APIRouter(prefix="/api")


class StartIn(BaseModel):
    context: Literal["mastery", "test_out"] = "mastery"


@router.post("/checks/{subtopic_id}/start")
def start_check(
    subtopic_id: str,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
    body: StartIn | None = None,
):
    sess, resumed = checks.start(
        db, content, user.id, subtopic_id, (body or StartIn()).context, now, key=key
    )
    out = checks.session_view(content, sess, resumed=resumed)
    db.commit()
    return out


class AnswerIn(BaseModel):
    session_id: int
    item_id: str
    elapsed_ms: int = Field(default=0, ge=0)  # editor time spent on this item
    session_elapsed_ms: int | None = Field(default=None, ge=0)  # absolute, like a heartbeat
    gave_up: bool = False  # the "Khong biet" button: recorded, never locks, never counts as a pass
    # write_code (the browser ran the hidden tests, like Submit)
    code: str | None = None
    language: str = "python"
    verdict: str | None = Field(default=None, min_length=1, max_length=16)
    passed_tests: int | None = Field(default=None, ge=0)
    total: int | None = Field(default=None, ge=0)
    runtime_ms: int | None = Field(default=None, ge=0)
    # read_code: the predicted output, graded on the server
    answer: str | None = None
    # concept: self-graded; recorded but never evidence for score 2/3
    self_grade: bool | None = None


@router.post("/checks/{subtopic_id}/answer")
def answer_check(
    subtopic_id: str,
    body: AnswerIn,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
):
    out = checks.answer(db, content, user.id, subtopic_id, body, now, key=key)
    db.commit()
    return out


class HeartbeatIn(BaseModel):
    elapsed_ms: int = Field(ge=0)  # absolute active time of the session, so a resend is safe


@router.post("/checks/{session_id}/heartbeat")
def heartbeat_check(session_id: int, body: HeartbeatIn, db: DB, user: User, now: Now, key: IdemKey):
    sess = checks.heartbeat(db, user.id, session_id, body.elapsed_ms, now)
    db.commit()
    return {
        "session_id": sess.id,
        "status": sess.status,
        "elapsed_ms": sess.elapsed_ms,
        "expires_at": checks.expires_iso(sess),
    }
