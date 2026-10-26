"""Placement assessment, Phase A (SPEC 5.6, UI_SPEC 2). See services/placement.py.

Write-code items run in the browser like a check Submit: the client posts verdict / passed_tests /
total. The server never sends the reference solution or the expected output.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..deps import DB, Content, IdemKey, Now, User
from ..errors import ApiError
from ..services import placement

router = APIRouter(prefix="/api")


class StartIn(BaseModel):
    experience: Literal["none", "some", "solid"] | None = None  # default: the saved profile
    restart: bool = False  # abandon a stale/unwanted sitting ("Làm lại từ đầu")
    skip: bool = False  # "Bắt đầu từ đầu": a skipped session, nothing is seeded


@router.post("/placement")
def start_placement(
    db: DB, user: User, content: Content, now: Now, key: IdemKey, body: StartIn | None = None
):
    b = body or StartIn()
    ps, resumed = placement.start(
        db,
        content,
        user.id,
        now,
        experience=b.experience,
        restart=b.restart,
        skip=b.skip,
        key=key,
    )
    out = placement.view(db, content, ps, resumed=resumed, now=now)
    db.commit()
    return out


@router.get("/placement/current")
def current_placement(db: DB, user: User, content: Content, now: Now):
    """The sitting in progress, else the latest finished/skipped one, else `{placement: null}`."""
    ps = placement.latest(db, user.id)
    if ps is None:
        return {"placement": None}
    return {"placement": placement.get(db, content, user.id, ps.id, now)}


@router.get("/placement/{placement_id}")
def get_placement(placement_id: int, db: DB, user: User, content: Content, now: Now):
    return placement.get(db, content, user.id, placement_id, now)


class AnswerIn(BaseModel):
    item_id: str
    elapsed_ms: int = Field(default=0, ge=0)  # time spent on this item
    session_elapsed_ms: int | None = Field(default=None, ge=0)  # absolute active time, as heartbeat
    gave_up: bool = False  # "Không biết": recorded, never locks, never a pass
    code: str | None = None
    language: str = "python"
    verdict: str | None = Field(default=None, min_length=1, max_length=16)
    passed_tests: int | None = Field(default=None, ge=0)
    total: int | None = Field(default=None, ge=0)
    runtime_ms: int | None = Field(default=None, ge=0)
    answer: str | None = None  # read_code (level 1)
    self_grade: bool | None = None  # concept (level 1)


@router.post("/placement/{placement_id}/answer")
def answer_placement(
    placement_id: int,
    body: AnswerIn,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
):
    out = placement.answer(db, content, user.id, placement_id, body, now, key=key)
    db.commit()
    return out


class SkipIn(BaseModel):
    item_id: str
    elapsed_ms: int = Field(default=0, ge=0)
    session_elapsed_ms: int | None = Field(default=None, ge=0)


@router.post("/placement/{placement_id}/skip")
def skip_placement_item(
    placement_id: int,
    body: SkipIn,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
):
    """ "Không biết" on the current item: a give-up (no lock, not a pass)."""
    full = AnswerIn(
        item_id=body.item_id,
        elapsed_ms=body.elapsed_ms,
        session_elapsed_ms=body.session_elapsed_ms,
        gave_up=True,
    )
    out = placement.answer(db, content, user.id, placement_id, full, now, key=key)
    db.commit()
    return out


class HeartbeatIn(BaseModel):
    active_ms: int = Field(ge=0)  # absolute active time of the sitting, so a resend is safe
    item_elapsed_ms: int | None = Field(default=None, ge=0)  # absolute, for the current item


@router.post("/placement/{placement_id}/heartbeat")
def heartbeat_placement(
    placement_id: int,
    body: HeartbeatIn,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
):
    out = placement.heartbeat(
        db, content, user.id, placement_id, body.active_ms, body.item_elapsed_ms, now
    )
    db.commit()
    return out


class FinishIn(BaseModel):
    active_ms: int | None = Field(default=None, ge=0)


@router.post("/placement/{placement_id}/finish")
def finish_placement(
    placement_id: int,
    db: DB,
    user: User,
    content: Content,
    now: Now,
    key: IdemKey,
    body: FinishIn | None = None,
):
    out = placement.finish(
        db, content, user.id, placement_id, (body or FinishIn()).active_ms, now, key=key
    )
    db.commit()
    return out


@router.get("/placement/{placement_id}/result")
def placement_result(placement_id: int, db: DB, user: User, content: Content):
    ps = placement._own(db, user.id, placement_id)
    if ps.status == "skipped":
        raise ApiError(409, "placement_skipped", "This placement was skipped; nothing was measured")
    return placement.result(db, content, user.id, placement_id)
