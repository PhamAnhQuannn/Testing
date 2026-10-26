"""Problems: statement, hints, solution, Submit token + hidden tests, attempts, drafts."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Header
from pydantic import BaseModel, Field
from sqlalchemy import select

from ..deps import DB, RT, Content, IdemKey, Now, User
from ..errors import ApiError
from ..models import tables as t
from ..services import progress
from ..services.content_loader import ProblemEntry
from .content import problem_status

router = APIRouter(prefix="/api")
MAX_HINTS = 3


def _problem(content, problem_id: str) -> ProblemEntry:
    p = content.problem(problem_id) or content.check_problem(problem_id)
    if p is None:
        raise ApiError(404, "problem_not_found", f"No problem {problem_id}")
    return p


def _state(db, user_id: int, problem_id: str, now: datetime) -> t.ProblemState:
    st = db.get(t.ProblemState, (user_id, problem_id))
    if st is None:
        st = t.ProblemState(
            user_id=user_id, problem_id=problem_id, hints_used=0, solution_viewed=False
        )
        db.add(st)
    return st


@router.get("/problems/{problem_id}")
def get_problem(problem_id: str, db: DB, user: User, content: Content):
    p = _problem(content, problem_id)
    out = content.public_problem(p)
    st = db.get(t.ProblemState, (user.id, problem_id))
    used = st.hints_used if st else 0
    out["hints"] = list(p.data.get("hints", []))[:used]  # only the ones already opened
    out["hints_used"] = used
    out["solution_viewed"] = bool(st and st.solution_viewed)
    out.update(problem_status(db, user.id, problem_id))
    last = db.scalar(
        select(t.Attempt)
        .where(t.Attempt.user_id == user.id, t.Attempt.problem_id == problem_id)
        .order_by(t.Attempt.id.desc())
        .limit(1)
    )
    out["last_attempt"] = (
        {
            "mode": last.mode,
            "verdict": last.verdict,
            "passed": last.passed,
            "total": last.total,
            "at": last.submitted_at.isoformat(),
        }
        if last
        else None
    )
    return out


@router.post("/problems/{problem_id}/hints")
def open_hint(problem_id: str, db: DB, user: User, content: Content, now: Now, key: IdemKey):
    p = _problem(content, problem_id)
    hints = list(p.data.get("hints", []))
    st = _state(db, user.id, problem_id, now)
    opened_now = None
    if (st.hints_used or 0) < min(MAX_HINTS, len(hints)):
        st.hints_used = (st.hints_used or 0) + 1
        opened_now = hints[st.hints_used - 1]
        progress.record_event(
            db,
            "hint_opened",
            {"problem_id": problem_id, "level": st.hints_used},
            now=now,
            idem_key=key,
        )
    db.commit()
    return {
        "hints_used": st.hints_used,
        "hint": opened_now,
        "hints": hints[: st.hints_used],
        "exhausted": st.hints_used >= min(MAX_HINTS, len(hints)),
    }


def _check_passed(db, user_id: int, content, problem_id: str) -> bool:
    found = content.check_item_of_problem(problem_id)
    if found is None:
        return False
    sid, item = found
    return (
        db.scalar(
            select(t.CheckResult.id)
            .where(
                t.CheckResult.user_id == user_id,
                t.CheckResult.subtopic_id == sid,
                t.CheckResult.item_id == item["id"],
                t.CheckResult.passed.is_(True),
            )
            .limit(1)
        )
        is not None
    )


@router.get("/problems/{problem_id}/solution")
def get_solution(problem_id: str, db: DB, user: User, content: Content, now: Now):
    p = _problem(content, problem_id)
    if p.data.get("kind") == "check" and not _check_passed(db, user.id, content, problem_id):
        # SPEC flow C: a failed (or not yet passed) check never reveals the reference solution
        raise ApiError(403, "check_solution_locked", "The reference is shown after passing it")
    st = _state(db, user.id, problem_id, now)
    if not st.solution_viewed:
        st.solution_viewed = True
        progress.record_event(db, "solution_viewed", {"problem_id": problem_id}, now=now)
    db.commit()
    return content.solution(p)


@router.post("/problems/{problem_id}/start-submit")
def start_submit(problem_id: str, content: Content, rt: RT):
    """Token (15 min) that unlocks GET /problems/{id}/tests/hidden for the browser runner."""
    _problem(content, problem_id)
    token, expires = rt.new_submit_token(problem_id)
    return {
        "token": token,
        "expires_at": expires.isoformat(),
        "ttl_s": rt.settings.submit_token_ttl_s,
    }


@router.get("/problems/{problem_id}/tests/hidden")
def hidden_tests(
    problem_id: str,
    content: Content,
    rt: RT,
    db: DB,
    token: str | None = None,
    x_submit_token: Annotated[str | None, Header()] = None,
):
    p = _problem(content, problem_id)
    rt.check_submit_token(x_submit_token or token, problem_id)
    return {
        "problem_id": problem_id,
        "problem_version": content.problem_version(db, problem_id),
        "limits": p.data["limits"],
        "tests": content.hidden_tests(p),
    }


# ---- attempts ----


class AttemptIn(BaseModel):
    problem_id: str
    mode: Literal["run", "submit"]
    language: str = "python"
    code: str
    verdict: str = Field(min_length=1, max_length=16)  # AC, WA, TLE, RE, CE, MLE...
    passed: int = Field(ge=0)
    total: int = Field(ge=0)
    elapsed_ms: int = Field(ge=0)
    runtime_ms: int | None = Field(default=None, ge=0)
    started_at: datetime | None = None
    occurred_at: datetime | None = None


@router.post("/attempts", status_code=201)
def post_attempt(body: AttemptIn, db: DB, user: User, content: Content, now: Now, key: IdemKey):
    p = _problem(content, body.problem_id)
    if body.passed > body.total:
        raise ApiError(422, "invalid_counts", "passed cannot exceed total")
    ac = body.verdict == "AC"
    if ac and body.passed != body.total:
        raise ApiError(422, "invalid_counts", "an AC verdict needs passed == total")
    st = _state(db, user.id, body.problem_id, now)
    draft = db.get(t.Draft, (user.id, body.problem_id, body.language))
    started = body.started_at or (draft.started_at if draft else None) or st.first_opened_at
    if st.first_opened_at is None:
        st.first_opened_at = started or now
    limit_ms = 1.5 * p.data["time_target_min"] * 60_000
    clean = (
        body.mode == "submit"
        and ac
        and not st.solution_viewed
        and (st.hints_used or 0) <= 1
        and body.elapsed_ms <= limit_ms
    )
    submitted = progress.clamp_occurred(body.occurred_at, now)
    attempt = t.Attempt(
        user_id=user.id,
        problem_id=body.problem_id,
        mode=body.mode,
        language=body.language,
        code=body.code,
        verdict=body.verdict,
        passed=body.passed,
        total=body.total,
        elapsed_ms=body.elapsed_ms,
        runtime_ms=body.runtime_ms,
        hints_used=st.hints_used or 0,
        solution_viewed=bool(st.solution_viewed),
        clean=clean,
        started_at=started,
        submitted_at=submitted,
        problem_version=content.problem_version(db, body.problem_id),
    )
    db.add(attempt)
    progress.record_event(
        db,
        "attempt",
        {
            "problem_id": body.problem_id,
            "mode": body.mode,
            "verdict": body.verdict,
            "passed": body.passed,
            "total": body.total,
            "elapsed_ms": body.elapsed_ms,
            "clean": clean,
        },
        now=now,
        occurred_at=body.occurred_at,
        idem_key=key,
    )
    db.flush()
    score: dict[str, Any] | None = None
    if body.mode == "submit":
        sid = p.subtopic_id
        info = progress.recompute_subtopic(db, content, sid, now, event_time=submitted)
        row = db.get(t.UserSubtopic, (user.id, sid))
        score = {
            "subtopic_id": sid,
            "before": info["before"],
            "after": info["after"],
            "status": row.status if row else None,
            "newly_unlocked": info["newly_unlocked"],
        }
    db.commit()
    return {
        "attempt_id": attempt.id,
        "verdict": body.verdict,
        "ac": ac and body.mode == "submit",
        "clean": clean,
        "hints_used": attempt.hints_used,
        "solution_viewed": attempt.solution_viewed,
        "elapsed_ms": body.elapsed_ms,
        "score": score,
    }


# ---- drafts ----


class DraftIn(BaseModel):
    code: str
    language: str = "python"
    updated_at: datetime
    cursor: dict | None = None
    elapsed_ms: int = Field(default=0, ge=0)
    started_at: datetime | None = None
    base_rev: int | None = None  # M3: ignored in M1


def _draft_json(d: t.Draft) -> dict[str, Any]:
    return {
        "problem_id": d.problem_id,
        "language": d.language,
        "code": d.code,
        "updated_at": d.updated_at.isoformat(),
        "cursor": d.cursor,
        "elapsed_ms": d.elapsed_ms,
        "started_at": d.started_at.isoformat() if d.started_at else None,
        "rev": d.rev,
    }


@router.put("/drafts/{problem_id}")
def put_draft(problem_id: str, body: DraftIn, db: DB, user: User, content: Content, now: Now):
    _problem(content, problem_id)
    updated = progress.clamp_occurred(body.updated_at, now)
    d = db.get(t.Draft, (user.id, problem_id, body.language))
    accepted = True
    if d is None:
        d = t.Draft(
            user_id=user.id,
            problem_id=problem_id,
            language=body.language,
            code=body.code,
            updated_at=updated,
            cursor=body.cursor,
            elapsed_ms=body.elapsed_ms,
            started_at=body.started_at or now,
            rev=1,
        )
        db.add(d)
    else:
        # Heartbeat values are absolute: the clock only moves forward, so keep the max.
        d.elapsed_ms = max(d.elapsed_ms or 0, body.elapsed_ms)
        if body.started_at and (d.started_at is None or body.started_at < d.started_at):
            d.started_at = body.started_at
        if updated >= d.updated_at:  # the newer copy wins (one device in M1)
            if body.code != d.code:
                d.rev += 1
            d.code = body.code
            d.cursor = body.cursor
            d.updated_at = updated
        else:
            accepted = False
    db.commit()
    return {"accepted": accepted, "draft": _draft_json(d)}


@router.get("/drafts/{problem_id}")
def get_draft(problem_id: str, db: DB, user: User, content: Content, language: str = "python"):
    _problem(content, problem_id)
    d = db.get(t.Draft, (user.id, problem_id, language))
    return {"draft": _draft_json(d) if d else None}
