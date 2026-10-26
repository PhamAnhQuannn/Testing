"""'Học tiếp' (SPEC 5.5) and the activity ping (SPEC 6.4)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from ..deps import DB, Content, Now, User
from ..services import next_up
from .resume import ResumeIn, _save

router = APIRouter(prefix="/api")


@router.get("/next")
def get_next(db: DB, user: User, content: Content, now: Now):
    return next_up.build_next(db, content, now, user.id)


class PingIn(BaseModel):
    resume: ResumeIn | None = None  # optional resume_state update, same rules as PUT /resume


@router.post("/activity/ping")
def activity_ping(db: DB, user: User, now: Now, body: PingIn | None = None):
    out = next_up.ping(db, user.id, now)
    db.commit()
    if body is not None and body.resume is not None:
        _save(db, body.resume, now, user.id)
    return out
