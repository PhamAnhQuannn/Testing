"""Leitner review (SPEC 5.4, 6.4): the due queue and the result of one card. See docs/API_M2A.md."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..deps import DB, Content, IdemKey, Now, User
from ..services import review

router = APIRouter(prefix="/api")


@router.get("/review/queue")
def review_queue(db: DB, user: User, content: Content, now: Now, editor: bool = True):
    return review.queue(db, content, now, user.id, editor=editor)


class ResultIn(BaseModel):
    success: bool
    # The item that was used. The kind is derived from the ref on the server (a known problem id =
    # code, anything else = recall); `item_kind` alone makes the server pick that kind's item.
    item_ref: str | None = Field(default=None, min_length=1, max_length=200)
    item_kind: Literal["code", "recall"] | None = None


@router.post("/review/{subtopic_id}/result")
def review_result(
    subtopic_id: str, body: ResultIn, db: DB, user: User, content: Content, now: Now, key: IdemKey
):
    out = review.apply_result(
        db,
        content,
        user.id,
        subtopic_id,
        success=body.success,
        item_ref=body.item_ref,
        item_kind=body.item_kind,
        now=now,
        key=key,
    )
    db.commit()
    return out
