"""Read side: /map, /subtopics, /lessons, /problems."""

from __future__ import annotations

from dataclasses import asdict
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Query
from sqlalchemy import func, select

from ..deps import DB, Content, Now, User
from ..errors import ApiError
from ..models import tables as t
from ..services import diagnosis, progress, unlock
from ..services.content_loader import TRACKS, ContentStore

router = APIRouter(prefix="/api")


def current_run(db, user_id: int, subtopic_id: str) -> int:
    return (
        db.scalar(
            select(func.max(t.LessonRun.run_no)).where(
                t.LessonRun.user_id == user_id, t.LessonRun.subtopic_id == subtopic_id
            )
        )
        or 1
    )


def problem_status(db, user_id: int, problem_id: str) -> dict[str, Any]:
    rows = db.scalars(
        select(t.Attempt).where(t.Attempt.user_id == user_id, t.Attempt.problem_id == problem_id)
    ).all()
    submits = [a for a in rows if a.mode == "submit"]
    solved = any(a.verdict == "AC" for a in submits)
    return {
        "status": "solved" if solved else ("attempted" if rows else "todo"),
        "solved_clean": any(a.verdict == "AC" and a.clean for a in submits),
        "attempts": len(rows),
    }


def _subtopic_item(
    sid: str,
    content: ContentStore,
    rows: dict[str, t.UserSubtopic],
    due: set[str],
    names: dict[str, str],
) -> dict[str, Any]:
    info = content.subtopics[sid]
    row = rows[sid]
    scores = {k: r.score for k, r in rows.items()}
    res = unlock.evaluate(
        info.get("prerequisites", []),
        content.assumed,
        set(content.subtopics),
        scores,
        row.unlocked_at,
    )
    plan_day = content.sort_key[sid][0]
    return {
        "id": sid,
        "name_vi": info["name_vi"],
        "section": info["section"],
        "module": info["module"],
        "order": info.get("plan_order") or info.get("order"),
        "plan_day": plan_day if plan_day < 10_000 else None,
        "est_hours": info.get("est_hours"),
        "target_intern": (info.get("target_swe") or {}).get("intern", 0),
        "prerequisites": info.get("prerequisites", []),
        "content_status": content.content_status(sid),
        "has_lesson": content.lesson(sid) is not None,
        "problem_count": len(content.problems_of(sid)),
        "score": row.score,
        "status": row.status,
        "unlocked": res.unlocked,
        "lock_reasons": [{**r, "name_vi": names.get(r["prerequisite"])} for r in res.reasons],
        "lesson_done": row.lesson_done_at is not None,
        "quiz_best": row.quiz_best,
        "tested_out": row.tested_out,
        "known_basic": row.known_basic,
        "due_cards": 1 if sid in due else 0,
    }


def _due_ids(db, user_id: int, today) -> set[str]:
    return set(
        db.scalars(
            select(t.ReviewCard.subtopic_id).where(
                t.ReviewCard.user_id == user_id,
                t.ReviewCard.due_on <= today,
                t.ReviewCard.suspended.is_(False),
            )
        )
    )


@router.get("/map")
def get_map(db: DB, user: User, content: Content, now: Now):
    rows = {
        r.subtopic_id: r
        for r in db.scalars(select(t.UserSubtopic).where(t.UserSubtopic.user_id == user.id))
    }
    today = progress.local_day(now, progress.user_tz(db, user.id))
    due = _due_ids(db, user.id, today)
    names = {k: v["name_vi"] for k, v in content.subtopics.items()}
    items = [
        _subtopic_item(sid, content, rows, due, names) for sid in content.ordered_subtopic_ids()
    ]
    return {
        "today": today.isoformat(),
        "assumed": sorted(content.assumed),
        "due_cards": len(due),
        "subtopics": items,
    }


@router.get("/subtopics/{subtopic_id}")
def get_subtopic(subtopic_id: str, db: DB, user: User, content: Content, now: Now):
    if subtopic_id not in content.subtopics:
        raise ApiError(404, "subtopic_not_found", f"Unknown subtopic {subtopic_id}")
    rows = {
        r.subtopic_id: r
        for r in db.scalars(select(t.UserSubtopic).where(t.UserSubtopic.user_id == user.id))
    }
    today = progress.local_day(now, progress.user_tz(db, user.id))
    names = {k: v["name_vi"] for k, v in content.subtopics.items()}
    out = _subtopic_item(subtopic_id, content, rows, _due_ids(db, user.id, today), names)
    info = content.subtopics[subtopic_id]
    out["summary_vi"] = info.get("summary_vi")
    out["mastery_bar_vi"] = info.get("mastery_bar_vi")
    lesson = content.lesson(subtopic_id)
    out["lesson"] = (
        {
            "version": lesson.data.get("version"),
            "est_minutes": lesson.data.get("est_minutes"),
            "objectives_vi": lesson.data.get("objectives_vi", []),
        }
        if lesson
        else None
    )
    practice = set((lesson.data.get("problems", {}).get("practice") if lesson else None) or [])
    out["problems"] = [
        {
            "id": p.id,
            "title": p.data["title"],
            "title_vi": p.data.get("title_vi"),
            "difficulty": p.data["difficulty"],
            "kind": p.data["kind"],
            "role": "practice" if p.id in practice else "extra",
            **problem_status(db, user.id, p.id),
        }
        for p in content.problems_of(subtopic_id)
    ]
    out["checks"] = [
        {"level": lvl, "item_id": i["id"], "type": i["type"], "minutes": i.get("minutes")}
        for lvl, items in content.check_items(subtopic_id).items()
        for i in items
    ]
    return out


@router.get("/lessons/{subtopic_id}")
def get_lesson(subtopic_id: str, db: DB, user: User, content: Content):
    lesson = content.lesson(subtopic_id)
    if lesson is None:
        raise ApiError(404, "lesson_not_found", f"No published lesson for {subtopic_id}")
    out = content.public_lesson(lesson)
    run_no = current_run(db, user.id, subtopic_id)
    answers: dict[str, Any] = {}
    for a in db.scalars(
        select(t.QuizAnswer)
        .where(
            t.QuizAnswer.user_id == user.id,
            t.QuizAnswer.quiz_item_id.like(f"{subtopic_id}#%"),
            t.QuizAnswer.run_no == run_no,
        )
        .order_by(t.QuizAnswer.attempt_no)
    ):
        block = a.quiz_item_id.split("#", 1)[1]
        e = answers.setdefault(block, {"attempts": 0, "first_correct": a.correct})
        e["attempts"] += 1
        e["last_answer"] = a.answer
        e["last_correct"] = a.correct
    row = db.get(t.UserSubtopic, (user.id, subtopic_id))
    out["progress"] = {
        "run_no": run_no,
        "answers": answers,
        "lesson_done": bool(row and row.lesson_done_at),
        "quiz_best": row.quiz_best if row else None,
        "score": row.score if row else 0,
        "known_basic": bool(row and row.known_basic),
    }
    return out


@router.get("/problems")
def list_problems(
    db: DB,
    user: User,
    content: Content,
    subtopic: str | None = None,
    difficulty: str | None = None,
    status: str | None = Query(default=None, pattern="^(todo|attempted|solved)$"),
    kind: str | None = None,
):
    out = []
    for p in content.problems.values():
        if content.problem(p.id) is None:
            continue
        d = p.data
        if subtopic and p.subtopic_id != subtopic:
            continue
        if difficulty and d["difficulty"] != difficulty:
            continue
        if kind and d["kind"] != kind:
            continue
        st = problem_status(db, user.id, p.id)
        if status and st["status"] != status:
            continue
        out.append(
            {
                "id": p.id,
                "subtopic_id": p.subtopic_id,
                "title": d["title"],
                "title_vi": d.get("title_vi"),
                "difficulty": d["difficulty"],
                "kind": d["kind"],
                "time_target_min": d["time_target_min"],
                "tags": d.get("tags", []),
                **st,
            }
        )
    out.sort(key=lambda x: (content.sort_key.get(x["subtopic_id"], (10_000, 0)), x["id"]))
    return {"problems": out}


ROLE_LABELS = {
    ("swe", "intern"): "SWE Intern",
    ("swe", "new_grad"): "SWE New Grad",
    ("ai", "intern"): "AI Engineer Intern",
    ("ai", "new_grad"): "AI Engineer New Grad",
}


def parse_role(role: str | None, settings: t.UserSettings | None) -> tuple[str, str]:
    """`swe-intern` style key -> (track, level); default from the user's settings."""
    if role is None:
        key = (
            (settings.track if settings else None) or "swe",
            (settings.target_role if settings else None) or "intern",
        )
        return key if key in ROLE_LABELS else ("swe", "intern")
    track, _, level = role.partition("-")
    if (track, level) not in ROLE_LABELS:
        raise ApiError(400, "invalid_role", f"Unknown role: {role}")
    return track, level


@router.get("/diagnosis")
def get_diagnosis(
    db: DB, user: User, content: Content, now: Now, role: str | None = Query(default=None)
):
    """Derived skill diagnosis (SPEC 5.7): read-only, never feeds scoring, unlock or Leitner."""
    track, level = parse_role(role, db.get(t.UserSettings, user.id))
    rows = {
        r.subtopic_id: r
        for r in db.scalars(select(t.UserSubtopic).where(t.UserSubtopic.user_id == user.id))
    }
    stale_before = now - timedelta(days=diagnosis.STALE_DAYS)
    views = []
    for sid in content.ordered_subtopic_ids():
        info = content.subtopics[sid]
        row = rows.get(sid)
        # "measured" = a real skill signal. A finished lesson is NOT one (reading != assessed), so
        # it is excluded: counting it would inflate coverage and drag the mean to 0 with no proof.
        measured = row is not None and (row.score > 0 or row.tested_out or row.known_basic)
        updated = row.updated_at if row else None
        if updated is not None and updated.tzinfo is None:
            updated = updated.replace(tzinfo=now.tzinfo)
        views.append(
            diagnosis.SubtopicView(
                id=sid,
                section=info["section"],
                module=info["module"],
                name_vi=info["name_vi"],
                score=row.score if row else 0,
                measured=measured,
                inferred_hint=row.placement_hint if row and not measured else None,
                has_lesson=content.lesson(sid) is not None,
                concepts=diagnosis.pick_concepts(info),
                target=int((info.get(f"target_{track}") or {}).get(level) or 0),
                stale=bool(measured and updated is not None and updated < stale_before),
            )
        )
    domains = diagnosis.diagnose(views, role=f"{track}-{level}")
    return {
        "tracks": TRACKS,
        "role": {
            "track": track,
            "level": level,
            "key": f"{track}-{level}",
            "label_vi": ROLE_LABELS[(track, level)],
        },
        **diagnosis.readiness_summary(domains, views),
        "domains": [asdict(d) for d in domains],
    }
