"""resume_state: where Quan stopped (SPEC 6.4, UI_SPEC 4.6)."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ValidationError
from sqlalchemy import select

from ..deps import DB, RT, Content, Now
from ..errors import ApiError
from ..models import tables as t
from ..services import progress

router = APIRouter(prefix="/api")


class ResumeIn(BaseModel):
    mode: Literal["lesson", "problem", "check", "placement", "review", "other"]
    route: str
    ref: dict[str, Any] = {}
    context: dict[str, Any] = {}
    device_id: str | None = None
    updated_at: datetime | None = None


def _json(r: t.ResumeState, stale: bool = False) -> dict[str, Any]:
    return {
        "mode": r.mode,
        "route": r.route,
        "ref": r.ref or {},
        "context": r.context or {},
        "updated_at": r.updated_at.isoformat(),
        "device_id": r.device_id,
        "stale": stale,
    }


def _is_stale(db, content, r: t.ResumeState, user_id: int) -> bool:
    ref = r.ref or {}
    if r.mode == "lesson" and ref.get("subtopic_id"):
        row = db.get(t.UserSubtopic, (user_id, ref["subtopic_id"]))
        info = content.subtopics.get(ref["subtopic_id"])
        if row and info:
            return row.status == "done"
    if r.mode == "problem" and ref.get("problem_id"):
        return (
            db.scalar(
                select(t.Attempt.id).where(
                    t.Attempt.user_id == user_id,
                    t.Attempt.problem_id == ref["problem_id"],
                    t.Attempt.mode == "submit",
                    t.Attempt.verdict == "AC",
                    t.Attempt.submitted_at > r.updated_at,
                )
            )
            is not None
        )
    return False


def _save(db, body: ResumeIn, now: datetime, user_id: int = progress.USER_ID) -> None:
    at = progress.clamp_occurred(body.updated_at, now)
    r = db.get(t.ResumeState, user_id)
    if r is not None and at < r.updated_at:
        return  # an older write (late beacon) never overwrites a newer position
    if r is None:
        r = t.ResumeState(user_id=user_id)
        db.add(r)
    r.mode, r.route, r.ref, r.context = body.mode, body.route, body.ref, body.context
    r.device_id, r.updated_at = body.device_id, at
    db.commit()


@router.put("/resume")
def put_resume(body: ResumeIn, db: DB, now: Now):
    _save(db, body, now)
    return {"ok": True}


@router.post("/resume")
async def post_resume(request: Request, db: DB, now: Now):
    """Same as PUT, for `navigator.sendBeacon` (any content type, no custom headers)."""
    try:
        body = ResumeIn.model_validate(json.loads(await request.body()))
    except (ValueError, ValidationError) as e:
        raise ApiError(422, "validation_error", f"Invalid resume body: {e}") from e
    _save(db, body, now)
    return {"ok": True}


@router.get("/resume")
def get_resume(db: DB, content: Content, rt: RT):
    uid = progress.USER_ID
    r = db.get(t.ResumeState, uid)
    primary = _json(r, _is_stale(db, content, r, uid)) if r else None
    others: list[dict[str, Any]] = []
    in_progress = db.scalars(
        select(t.UserSubtopic)
        .where(t.UserSubtopic.user_id == uid, t.UserSubtopic.status == "in_progress")
        .order_by(t.UserSubtopic.updated_at.desc())
    ).all()
    for row in in_progress:
        if primary and primary["ref"].get("subtopic_id") == row.subtopic_id:
            continue
        others.append(
            {
                "mode": "lesson",
                "route": f"/s/{row.subtopic_id}",
                "ref": {"subtopic_id": row.subtopic_id},
                "name_vi": content.subtopics[row.subtopic_id]["name_vi"],
            }
        )
        if len(others) >= 3:
            break
    return {
        "primary": primary,
        "others": others,
        "in_progress": {"placement": None, "check": None, "review": None},
    }
