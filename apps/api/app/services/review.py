"""Leitner review queue and result (SPEC 5.4). Rules live in `leitner.py` (pure); this module
assembles the queue, picks the item of each card and applies a result."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..errors import ApiError
from ..models import tables as t
from . import leitner, progress
from .content_loader import ContentStore

PRESET_DEFAULT = 6
PRESET_MAX_CODE = 2


def _recall_candidates(content: ContentStore, sid: str) -> list[dict[str, Any]]:
    """Quick-recall items: graded lesson blocks (quiz / predict_output), then level-1 check items
    that are not write_code (read_code / concept)."""
    out: list[dict[str, Any]] = []
    lesson = content.lesson(sid)
    if lesson:
        for ref in lesson.graded_ids():
            block = lesson.block(ref.split("#", 1)[1]) or {}
            out.append(
                {"kind": "recall", "ref": ref, "type": block.get("type"), "subtopic_id": sid}
            )
    for item in content.check_items(sid)[1]:
        if item.get("type") != "write_code":
            out.append(
                {
                    "kind": "recall",
                    "ref": f"check:{sid}:{item['id']}",
                    "type": item.get("type"),
                    "subtopic_id": sid,
                }
            )
    return out


def _code_candidates(db: Session, content: ContentStore, sid: str, user_id: int) -> list[str]:
    """Short code problems: level-2/3 check problems, then practice problems. Not-yet-clean first,
    then the one seen longest ago (SPEC 5.4 rule 4)."""
    ids: list[str] = []
    for level in (2, 3):
        for item in content.check_items(sid)[level]:
            pid = item.get("problem_id")
            if item.get("type") == "write_code" and pid and content.check_problem(pid):
                ids.append(pid)
    lesson = content.lesson(sid)
    if lesson:
        for pid in lesson.data.get("problems", {}).get("practice", []):
            if content.problem(pid):
                ids.append(pid)
    ids = list(dict.fromkeys(ids))
    if not ids:
        return []
    clean: set[str] = set()
    last: dict[str, datetime] = {}
    for a in db.scalars(
        select(t.Attempt).where(t.Attempt.user_id == user_id, t.Attempt.problem_id.in_(ids))
    ):
        if a.verdict == "AC" and a.clean and a.mode == "submit":
            clean.add(a.problem_id)
        seen = a.submitted_at.replace(tzinfo=None)
        if a.problem_id not in last or seen > last[a.problem_id]:
            last[a.problem_id] = seen
    order = {pid: n for n, pid in enumerate(ids)}

    def key(pid: str) -> tuple[bool, datetime, int]:
        return (pid in clean, last.get(pid, datetime.min), order[pid])

    return sorted(ids, key=key)


def _pick_recall(
    db: Session, content: ContentStore, sid: str, user_id: int
) -> dict[str, Any] | None:
    cands = _recall_candidates(content, sid)
    if not cands:
        return None
    n = len(
        db.scalars(
            select(t.ReviewLog.id).where(
                t.ReviewLog.user_id == user_id, t.ReviewLog.subtopic_id == sid
            )
        ).all()
    )
    return cands[n % len(cands)]  # rotate, so the same question is not asked every time


def _pick_code(db: Session, content: ContentStore, sid: str, user_id: int) -> dict[str, Any] | None:
    pids = _code_candidates(db, content, sid, user_id)
    if not pids:
        return None
    return {"kind": "code", "ref": pids[0], "type": "write_code", "subtopic_id": sid}


def pick_item(
    db: Session, content: ContentStore, card: t.ReviewCard, *, editor: bool = True
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """(item, recall_fallback): boxes 1-2 recall; boxes 3-5 a code problem when there is an editor
    and one exists (else recall). `recall_fallback` is set for boxes 3-5 (short-session preset)."""
    sid, uid = card.subtopic_id, card.user_id
    recall = _pick_recall(db, content, sid, uid)
    if leitner.item_kind_for_box(card.box, device_has_editor=editor) == "code":
        code = _pick_code(db, content, sid, uid)
        if code:
            return code, recall
    return recall, recall if card.box >= 3 else None


def today(db: Session, now: datetime, user_id: int) -> date:
    return progress.local_day(now, progress.user_tz(db, user_id))


def queue(
    db: Session, content: ContentStore, now: datetime, user_id: int, *, editor: bool = True
) -> dict[str, Any]:
    day = today(db, now, user_id)
    rows = db.execute(
        select(t.ReviewCard, t.UserSubtopic.score)
        .outerjoin(
            t.UserSubtopic,
            (t.UserSubtopic.user_id == t.ReviewCard.user_id)
            & (t.UserSubtopic.subtopic_id == t.ReviewCard.subtopic_id),
        )
        .where(
            t.ReviewCard.user_id == user_id,
            t.ReviewCard.due_on <= day,
            t.ReviewCard.suspended.is_(False),
        )
    ).all()
    ordered = sorted(rows, key=lambda r: (r[0].due_on, r[1] or 0, r[0].subtopic_id))
    cards: list[dict[str, Any]] = []
    for card, score in ordered:
        item, recall = pick_item(db, content, card, editor=editor)
        info = content.subtopics.get(card.subtopic_id, {})
        cards.append(
            {
                "subtopic_id": card.subtopic_id,
                "name_vi": info.get("name_vi"),
                "box": card.box,
                "due_on": card.due_on.isoformat(),
                "overdue_days": (day - card.due_on).days,
                "score": score or 0,
                "lapses": card.lapses,
                "item_kind": item["kind"] if item else None,
                "item": item,
                "recall_item": recall,
            }
        )
    settings = db.get(t.UserSettings, user_id)
    preset = settings.review_preset if settings else PRESET_DEFAULT
    warn = settings.backlog_warn if settings else 20
    return {
        "today": day.isoformat(),
        "total_due": len(cards),
        "backlog_warn": warn,
        "backlog": len(cards) > warn,
        "cards": cards,  # the WHOLE due list: no server-side cap (SPEC 5.4 rule 5)
        "short_session": _short_session(cards, preset),
    }


def _short_session(cards: list[dict[str, Any]], size: int | None) -> dict[str, Any]:
    """Data for the optional "Phiên ngắn" preset; the server never trims the queue with it."""
    if size is None:
        return {"enabled": False, "size": None, "max_code": PRESET_MAX_CODE, "cards": []}
    picked: list[dict[str, Any]] = []
    code = 0
    for c in cards[:size]:
        kind = c["item_kind"]
        if kind == "code":
            if code < PRESET_MAX_CODE:
                code += 1
            else:
                kind = "recall" if c["recall_item"] else None
        picked.append({"subtopic_id": c["subtopic_id"], "item_kind": kind})
    return {"enabled": True, "size": size, "max_code": PRESET_MAX_CODE, "cards": picked}


def apply_result(
    db: Session,
    content: ContentStore,
    user_id: int,
    subtopic_id: str,
    *,
    success: bool,
    item_ref: str | None,
    item_kind: str | None,
    now: datetime,
    key: str | None,
) -> dict[str, Any]:
    card = db.get(t.ReviewCard, (user_id, subtopic_id))
    if card is None:
        raise ApiError(404, "review_card_not_found", "No review card for this subtopic")
    day = today(db, now, user_id)
    if card.suspended or card.due_on > day:
        raise ApiError(409, "card_not_due", "This card is not due", due_on=card.due_on.isoformat())

    if item_ref is not None:
        derived = "code" if item_ref in content.problems else "recall"
        if item_kind is not None and item_kind != derived:
            raise ApiError(422, "item_kind_mismatch", f"item_ref is a {derived} item")
        kind = derived
    else:
        if item_kind is None:
            raise ApiError(422, "missing_field", "item_ref or item_kind is required")
        if item_kind == "code":
            picked = _pick_code(db, content, subtopic_id, user_id)
        else:
            picked = _pick_recall(db, content, subtopic_id, user_id)
        if picked is None:
            raise ApiError(422, "no_review_item", f"No {item_kind} item for this subtopic")
        item_ref, kind = picked["ref"], item_kind

    before = leitner.Card(card.box, card.due_on, card.lapses, card.consecutive_passes)
    after = leitner.review(before, success, day)  # from the REAL review day
    db.add(
        t.ReviewLog(
            user_id=user_id,
            subtopic_id=subtopic_id,
            item_ref=item_ref,
            item_kind=kind,
            box_before=before.box,
            box_after=after.box,
            success=success,
            reviewed_at=now,
        )
    )
    card.box, card.due_on = after.box, after.due_on
    card.lapses, card.consecutive_passes = after.lapses, after.consecutive_passes
    card.last_reviewed_at = now
    card.current_item_ref = None
    card.current_item_opened_at = None
    progress.record_event(
        db,
        "review_result",
        {
            "subtopic_id": subtopic_id,
            "item_ref": item_ref,
            "item_kind": kind,
            "success": success,
            "box_before": before.box,
            "box_after": after.box,
        },
        now=now,
        idem_key=key,
        user_id=user_id,
    )
    res = progress.recompute_subtopic(db, content, subtopic_id, now, user_id=user_id)
    return {
        "subtopic_id": subtopic_id,
        "success": success,
        "item_ref": item_ref,
        "item_kind": kind,
        "box_before": before.box,
        "box_after": after.box,
        "due_on": after.due_on.isoformat(),
        "lapses": after.lapses,
        "score": {"before": res["before"], "after": res["after"]},
        "newly_unlocked": res["newly_unlocked"],
    }
