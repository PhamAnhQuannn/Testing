"""'Học tiếp' (SPEC 5.5): what to study next, and `study_time` (SPEC 6.4 `/activity/ping`).

No current day, no schedule comparison, no quota: the order is the plan key `(N, position)` and
the user's own progress. Nothing here changes a score or an unlock.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import tables as t
from . import checks, progress, unlock
from . import scoring as sc
from .content_loader import ContentStore

PING_CAP_S = 60
PING_MAX_GAP_S = 120
LOCKED_PREVIEW = 3
MUST_RAISE_MAX = 5


# ---- study_time ----


def _week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())  # Monday


def study_totals(db: Session, user_id: int, day: date) -> dict[str, int]:
    today_s = db.scalar(
        select(t.StudyTime.seconds).where(t.StudyTime.user_id == user_id, t.StudyTime.day == day)
    )
    week_s = db.scalar(
        select(func.coalesce(func.sum(t.StudyTime.seconds), 0)).where(
            t.StudyTime.user_id == user_id,
            t.StudyTime.day >= _week_start(day),
            t.StudyTime.day <= day,
        )
    )
    return {"today_s": today_s or 0, "week_s": int(week_s or 0)}


def ping(db: Session, user_id: int, now: datetime) -> dict[str, Any]:
    """Add min(now - last_ping, 60 s) to today's study time; a gap over 2 minutes adds nothing.

    `last_ping` is per user, so several tabs never double count. The caller commits.
    """
    day = progress.local_day(now, progress.user_tz(db, user_id))
    state = db.get(t.ActivityState, user_id)
    added = 0
    if state is None:
        db.add(t.ActivityState(user_id=user_id, last_ping_at=now))
    else:
        gap = (now - state.last_ping_at).total_seconds()
        if 0 < gap <= PING_MAX_GAP_S:
            added = int(min(gap, PING_CAP_S))
        if gap > 0:
            state.last_ping_at = now  # never moves backwards (a late, out-of-order ping)
    if added:
        row = db.get(t.StudyTime, (user_id, day))
        if row is None:
            db.add(t.StudyTime(user_id=user_id, day=day, seconds=added))
        else:
            row.seconds += added
    db.flush()
    return {"added_s": added, **study_totals(db, user_id, day)}


# ---- /next ----


def _solved_ids(db: Session, user_id: int) -> set[str]:
    return set(
        db.scalars(
            select(t.Attempt.problem_id)
            .where(
                t.Attempt.user_id == user_id,
                t.Attempt.mode == "submit",
                t.Attempt.verdict == "AC",
            )
            .distinct()
        )
    )


def suggest_problem(content: ContentStore, sid: str, solved: set[str]) -> dict[str, Any] | None:
    """First `practice` problem not yet Accepted, then an `extra` one (SPEC 5.5)."""
    lesson = content.lesson(sid)
    practice = list(((lesson.data.get("problems") or {}).get("practice") or []) if lesson else [])
    extra = [
        p.id
        for p in content.problems_of(sid)
        if p.id not in practice and p.data.get("kind") != "check"
    ]
    for role, ids in (("practice", practice), ("extra", extra)):
        for pid in ids:
            entry = content.problem(pid)
            if entry is None or pid in solved:
                continue
            d = entry.data
            return {
                "id": pid,
                "title": d["title"],
                "title_vi": d.get("title_vi"),
                "difficulty": d["difficulty"],
                "role": role,
            }
    return None


def _check_lock(db: Session, user_id: int, sid: str, now: datetime) -> str | None:
    level = 3 if checks.level_passed(db, user_id, sid, 2) else 2
    until = checks.retry_after(db, user_id, sid, level, now)
    return until.isoformat() if until else None


def build_next(db: Session, content: ContentStore, now: datetime, user_id: int) -> dict[str, Any]:
    rows = {
        r.subtopic_id: r
        for r in db.scalars(select(t.UserSubtopic).where(t.UserSubtopic.user_id == user_id))
    }
    scores = {k: r.score for k, r in rows.items()}
    ids = set(content.subtopics)
    day = progress.local_day(now, progress.user_tz(db, user_id))
    solved = _solved_ids(db, user_id)
    due = set(
        db.scalars(
            select(t.ReviewCard.subtopic_id).where(
                t.ReviewCard.user_id == user_id,
                t.ReviewCard.due_on <= day,
                t.ReviewCard.suspended.is_(False),
            )
        )
    )

    def brief(sid: str) -> dict[str, Any]:
        return {"id": sid, "name_vi": content.subtopics[sid]["name_vi"]}

    up: list[tuple[tuple[int, tuple[int, int]], dict[str, Any]]] = []
    locked: list[tuple[str, unlock.Unlock]] = []
    for sid in content.ordered_subtopic_ids():
        info = content.subtopics[sid]
        row = rows.get(sid)
        if row is None:
            continue
        res = unlock.evaluate(
            info.get("prerequisites", []), content.assumed, ids, scores, row.unlocked_at
        )
        if not (res.unlocked or row.tested_out):
            locked.append((sid, res))
            continue
        target = (info.get("target_swe") or {}).get("intern", 0)
        if sc.is_done(row.score, target):
            continue
        started = row.status == unlock.IN_PROGRESS or row.score > 0
        retry = _check_lock(db, user_id, sid, now) if started else None
        group = 2 if retry else (0 if started else 1)
        up.append(
            (
                (group, content.sort_key[sid]),
                {
                    **brief(sid),
                    "score": row.score,
                    "target_intern": target,
                    "status": unlock.IN_PROGRESS if started else unlock.UNLOCKED,
                    "known_basic": row.known_basic,
                    "lesson_done": row.lesson_done_at is not None,
                    "has_lesson": content.lesson(sid) is not None,
                    "check_retry_after": retry,
                    "due_card": sid in due,
                    "suggested_problem": suggest_problem(content, sid, solved),
                },
            )
        )
    up.sort(key=lambda x: x[0])

    # Group 1: a prerequisite the user has started (score 1) but which is still below 2, which
    # keeps a later subtopic shut. It never changes `done` (SPEC 5.5).
    must: dict[str, dict[str, Any]] = {}
    for sid, res in locked:
        for r in res.reasons:
            p = r["prerequisite"]
            prow = rows.get(p)
            if r.get("missing_content") or prow is None or p not in ids:
                continue
            if prow.score != 1:
                continue  # 0 = not started (it is in the list below); >= 2 never blocks
            if p in must:
                must[p]["also_blocks"] += 1
                continue
            must[p] = {
                "prerequisite": {**brief(p), "score": prow.score, "need": 2},
                "unlocks": brief(sid),
                "sole_blocker": len(res.reasons) == 1,
                "also_blocks": 0,
                "suggested_problem": suggest_problem(content, p, solved),
                "test_out": {
                    "available": bool(content.check_items(p).get(2)),
                    "retry_after": _check_lock(db, user_id, p, now),
                },
            }
    must_raise = list(must.values())[:MUST_RAISE_MAX]

    preview = [
        {
            **brief(sid),
            "lock_reasons": [
                {**r, "name_vi": content.subtopics.get(r["prerequisite"], {}).get("name_vi")}
                for r in res.reasons
            ],
        }
        for sid, res in locked
    ][:LOCKED_PREVIEW]

    s = db.get(t.UserSettings, user_id)
    backlog_warn = s.backlog_warn if s else 20
    return {
        "must_raise": must_raise,
        "up_next": [item for _, item in up],
        "locked_preview": preview,
        "due_count": len(due),
        "backlog": len(due) > backlog_warn,
        "study": study_totals(db, user_id, day),
    }
