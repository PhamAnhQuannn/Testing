"""Event recording and the recompute of `user_subtopic` / unlocks / review cards.

Every public function here runs inside the caller's transaction (one transaction per event,
SPEC 6.7): the event row and the derived cache rows are committed together or not at all.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import tables as t
from . import leitner, unlock
from . import scoring as sc
from .content_loader import ContentStore

USER_ID = 1
MAX_PAST = timedelta(days=7)
MAX_FUTURE = timedelta(minutes=5)


def clamp_occurred(occurred: datetime | None, now: datetime) -> datetime:
    """Client time clamped to [received - 7 days, received + 5 minutes] (SPEC 4.4)."""
    if occurred is None:
        return now
    if occurred.tzinfo is None:
        occurred = occurred.replace(tzinfo=UTC)
    return min(max(occurred, now - MAX_PAST), now + MAX_FUTURE)


def local_day(moment: datetime, tz: str) -> date:
    return moment.astimezone(ZoneInfo(tz)).date()


def user_tz(db: Session, user_id: int = USER_ID) -> str:
    s = db.get(t.UserSettings, user_id)
    return s.tz if s else "Asia/Ho_Chi_Minh"


def record_event(
    db: Session,
    type_: str,
    payload: dict[str, Any],
    *,
    now: datetime,
    occurred_at: datetime | None = None,
    idem_key: str | None = None,
    user_id: int = USER_ID,
) -> t.Event:
    ev = t.Event(
        user_id=user_id,
        type=type_,
        payload=payload,
        ts=now,
        occurred_at=clamp_occurred(occurred_at, now),
        received_at=now,
        idem_key=idem_key,
    )
    db.add(ev)
    db.flush()
    return ev


# ---- evidence -> score ----


def load_evidence(
    db: Session, content: ContentStore, subtopic_id: str, user_id: int = USER_ID
) -> sc.Evidence:
    lesson_done = any(
        e.payload.get("subtopic_id") == subtopic_id
        for e in db.scalars(
            select(t.Event).where(t.Event.user_id == user_id, t.Event.type == "lesson_done")
        )
    )
    answers = tuple(
        sc.QuizAnswerEv(a.quiz_item_id, a.run_no, a.attempt_no, a.correct)
        for a in db.scalars(
            select(t.QuizAnswer).where(
                t.QuizAnswer.user_id == user_id,
                t.QuizAnswer.quiz_item_id.like(f"{subtopic_id}#%"),
            )
        )
    )
    pids = [p.id for p in content.problems.values() if p.subtopic_id == subtopic_id]
    attempts: tuple[sc.AttemptEv, ...] = ()
    if pids:
        attempts = tuple(
            sc.AttemptEv(a.problem_id, a.verdict == "AC", a.clean)
            for a in db.scalars(
                select(t.Attempt).where(
                    t.Attempt.user_id == user_id,
                    t.Attempt.mode == "submit",
                    t.Attempt.problem_id.in_(pids),
                )
            )
        )
    checks = tuple(
        sc.CheckEv(c.item_id, c.level, c.passed, c.clean, c.gave_up, c.item_type)
        for c in db.scalars(
            select(t.CheckResult).where(
                t.CheckResult.user_id == user_id, t.CheckResult.subtopic_id == subtopic_id
            )
        )
    )
    reviews = tuple(
        sc.ReviewEv(r.success, r.box_before, r.item_kind)
        for r in db.scalars(
            select(t.ReviewLog).where(
                t.ReviewLog.user_id == user_id, t.ReviewLog.subtopic_id == subtopic_id
            )
        )
    )
    return sc.Evidence(lesson_done, answers, attempts, checks, reviews)


def compute_score(
    db: Session, content: ContentStore, subtopic_id: str, user_id: int = USER_ID
) -> sc.ScoreResult:
    return sc.score(content.spec_for(subtopic_id), load_evidence(db, content, subtopic_id, user_id))


def ensure_user_rows(db: Session, content: ContentStore, now: datetime) -> None:
    if db.get(t.User, USER_ID) is None:
        db.add(t.User(id=USER_ID, name="Quan", created_at=now))
        db.flush()
    if db.get(t.UserSettings, USER_ID) is None:
        db.add(t.UserSettings(user_id=USER_ID))
    have = set(
        db.scalars(select(t.UserSubtopic.subtopic_id).where(t.UserSubtopic.user_id == USER_ID))
    )
    for sid in content.subtopics:
        if sid not in have:
            db.add(t.UserSubtopic(user_id=USER_ID, subtopic_id=sid))
    db.flush()


def _activity_ids(db: Session, content: ContentStore, user_id: int) -> set[str]:
    ids: set[str] = set()
    for (qid,) in db.execute(
        select(t.QuizAnswer.quiz_item_id).where(t.QuizAnswer.user_id == user_id).distinct()
    ):
        ids.add(qid.split("#", 1)[0])
    pmap = {p.id: p.subtopic_id for p in content.problems.values()}
    for (pid,) in db.execute(
        select(t.Attempt.problem_id).where(t.Attempt.user_id == user_id).distinct()
    ):
        if pid in pmap:
            ids.add(pmap[pid])
    for (sid,) in db.execute(
        select(t.LessonRun.subtopic_id).where(t.LessonRun.user_id == user_id).distinct()
    ):
        ids.add(sid)
    return ids


def sync_unlocks(
    db: Session, content: ContentStore, now: datetime, user_id: int = USER_ID
) -> list[str]:
    """Write `unlocked_at` the first time a subtopic becomes unlocked (never cleared) and refresh
    `status`. Returns ids newly unlocked."""
    rows = {
        r.subtopic_id: r
        for r in db.scalars(select(t.UserSubtopic).where(t.UserSubtopic.user_id == user_id))
    }
    scores = {sid: r.score for sid, r in rows.items()}
    active = _activity_ids(db, content, user_id)
    content_ids = set(content.subtopics)
    newly: list[str] = []
    for sid, info in content.subtopics.items():
        row = rows.get(sid)
        if row is None:
            continue
        res = unlock.evaluate(
            info.get("prerequisites", []), content.assumed, content_ids, scores, row.unlocked_at
        )
        new_at = unlock.newly_unlocked(res, row.unlocked_at, now, tested_out=row.tested_out)
        if row.unlocked_at is None and new_at is not None:
            row.unlocked_at = new_at
            newly.append(sid)
        target = (info.get("target_swe") or {}).get("intern", 0)
        row.status = unlock.status(
            new_at is not None,
            row.score,
            target,
            has_activity=sid in active or row.lesson_done_at is not None,
            blocked_missing_content=res.blocked_missing_content,
        )
    db.flush()
    return newly


def recompute_subtopic(
    db: Session,
    content: ContentStore,
    subtopic_id: str,
    now: datetime,
    *,
    event_time: datetime | None = None,
    user_id: int = USER_ID,
) -> dict[str, Any]:
    """Recompute the cache row of one subtopic from events, then cascade unlocks.

    Returns {before, after, newly_unlocked, review_card_created}.
    """
    row = db.get(t.UserSubtopic, (user_id, subtopic_id))
    if row is None:
        row = t.UserSubtopic(user_id=user_id, subtopic_id=subtopic_id)
        db.add(row)
    before = row.score
    res = compute_score(db, content, subtopic_id, user_id)
    row.score = res.score
    row.quiz_best = res.quiz_best
    row.tested_out = res.tested_out
    row.updated_at = now
    done_ev = db.scalars(
        select(t.Event)
        .where(t.Event.user_id == user_id, t.Event.type == "lesson_done")
        .order_by(t.Event.occurred_at)
    ).all()
    mine = [e for e in done_ev if e.payload.get("subtopic_id") == subtopic_id]
    row.lesson_done_at = mine[0].occurred_at if mine else None
    if row.placement_hint is not None and (res.score > 0 or row.lesson_done_at is not None):
        row.placement_hint = None  # real evidence replaces a graph-inferred label (SPEC 5.6 #5)
    db.flush()

    created = False
    if res.score >= 1 and db.get(t.ReviewCard, (user_id, subtopic_id)) is None:
        # the event that first made the score >= 1 (lesson_done or a check pass)
        card = leitner.new_card(local_day(event_time or now, user_tz(db, user_id)))
        db.add(
            t.ReviewCard(
                user_id=user_id,
                subtopic_id=subtopic_id,
                box=card.box,
                due_on=card.due_on,
            )
        )
        created = True
    newly = sync_unlocks(db, content, now, user_id)
    return {
        "before": before,
        "after": res.score,
        "newly_unlocked": newly,
        "review_card_created": created,
    }


def recompute_all(db: Session, content: ContentStore, now: datetime) -> None:
    """Rebuild every score cache from the event tables (used by tests and a future `repair`)."""
    for sid in content.subtopics:
        recompute_subtopic(db, content, sid, now)
