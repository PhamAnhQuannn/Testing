"""Placement, Phase A (SPEC 5.6, UI_SPEC 2): the gate ladder C1-C7 + stop rules + time budget.

Placement is a mastery check ordered by the prerequisite graph. It writes ONLY `check_results`
(context=placement) through the same `checks.answer` flow; the score is recomputed from events by
`scoring.py`, so it can never be 1 or 3: a clean level-2 `write_code` pass is `tested_out` (2), a
level-3 item is never asked here, and a level-1 pass only sets `known_basic`. Graph inference is a
label (`user_subtopic.placement_hint`) and never a score. "Start from scratch" writes nothing.

Phase A: one gate item per gate (the cluster's gate subtopic, level 2 `write_code`, 6 minutes).
`experience` picks the entry gate (none -> C1, some -> C2, solid -> C3); `none` only ever runs
C1 -> C2. A pass asks the next gate up. A failed or given-up gate stops the run once the gate right
below it has been tried (asking exactly that one gate if it was not measured yet), or at once when
there is no gate below. A gate that fails (E2) goes down to a level-1 diagnostic item (E1) when it
has one. The one-sitting budget is 45 min soft / 60 min hard of ACTIVE time (client heartbeats,
absolute and monotonic); Phase A uses the hard one: no new gate when active + cost > 60 min.
"""

from __future__ import annotations

import copy
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..errors import ApiError
from ..models import tables as t
from . import checks, progress
from .content_loader import ContentStore

SOFT_MS = 45 * 60_000
HARD_MS = 60 * 60_000
ACTIVE_SLACK_MS = 15_000  # reported active time may not outrun the wall clock by more than this
STALE_AFTER = timedelta(days=7)

# (code, gate subtopic, gate item, name_vi), in difficulty order (UI_SPEC 2.2, assessment clusters)
GATES: list[tuple[str, str, str, str]] = [
    ("C1", "py.core.strings", "Q012", "Python căn bản"),
    ("C2", "py.datastructs.dict", "Q023", "Cấu trúc dữ liệu Python, hàm, Big-O"),
    ("C3", "dsa.arrays_strings.hash_tables", "Q258", "Mảng, chuỗi, hash, prefix sum"),
    ("C4", "dsa.two_pointers_window.two_pointers", "Q070", "Hai con trỏ, cửa sổ trượt"),
    ("C5", "dsa.linked_list.ll_basics", "Q079", "Class, linked list, stack/queue"),
    ("C6", "dsa.searching_sorting.binary_search_basics", "Q095", "Binary search, sorting"),
    ("C7", "dsa.trees.tree_basics", "Q105", "Cây, heap, design, intervals"),
]
ENTRY = {"none": 0, "some": 1, "solid": 2}
LAST_GATE = {"none": 1, "some": 6, "solid": 6}  # `none` only runs C1 -> C2 (UI_SPEC 2.4 A1)

PASS_LIKE = {"passed", "passed_unclean", "known"}
FAIL_LIKE = {"failed", "gave_up", "locked"}

MESSAGES = {
    "failed_start": "Chưa cần đo thêm; bắt đầu từ nền tảng sẽ hiệu quả hơn.",
    "two_fails": "Chưa cần đo thêm; bắt đầu từ nền tảng sẽ hiệu quả hơn.",
    "fail_after_pass": "Đã tìm được ranh giới trình độ của bạn.",
    "all_gates": "Bạn đã qua tất cả các cổng đánh giá.",
    "entry_gates_done": "Đã đo xong phần nền tảng.",
    "budget": "Đã hết thời gian đánh giá của lần này.",
    "user_finished": "Bạn đã kết thúc sớm; kết quả đã đo được giữ lại.",
    "no_gates": "Chưa có cổng đánh giá nào sẵn sàng.",
}


# ---- helpers ----


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() if moment else None


def _gate_item(content: ContentStore, subtopic_id: str, item_id: str) -> dict[str, Any] | None:
    """The gate's E2: the named item, else the shortest non-weekly level-2 write_code item."""
    items = [
        i
        for i in content.check_items(subtopic_id)[2]
        if i["type"] == "write_code" and content.check_problem(i.get("problem_id") or "")
    ]
    for i in items:
        if i["id"] == item_id:
            return i
    curated = {i["id"] for i in content.curated_check_items(subtopic_id)[2]}
    pool = [i for i in items if not i["id"].startswith("W")]
    pool = [i for i in pool if i["id"] in curated] or pool  # prefer the lesson's curated gate
    return min(pool, key=lambda i: i.get("minutes") or 8) if pool else None


def _build_gates(
    db: Session, content: ContentStore, user_id: int, now: datetime
) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for code, sid, item_id, name in GATES:
        g: dict[str, Any] = {
            "code": code,
            "subtopic_id": sid,
            "name_vi": name,
            "item_id": None,
            "minutes": 6,
            "outcome": None,
            "check_session_id": None,
            "l1": None,
            "retry_after": None,
        }
        item = _gate_item(content, sid, item_id) if sid in content.subtopics else None
        if item is None:
            g["outcome"] = "unavailable"  # not placeable (no level-2 write_code check problem)
        else:
            g["item_id"] = item["id"]
            g["minutes"] = item.get("minutes") or 8
            row = db.get(t.UserSubtopic, (user_id, sid))
            if (row and row.score >= 2) or checks.level_passed(db, user_id, sid, 2):
                g["outcome"] = "known"  # already >= 2: nothing to add (UI_SPEC 2.2)
            else:
                until = checks.retry_after(db, user_id, sid, 2, now)
                if until is not None:
                    g["outcome"] = "locked"
                    g["retry_after"] = until.isoformat()
        gates.append(g)
    return gates


def _graph(content: ContentStore) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    ids = set(content.subtopics)
    up = {
        sid: [p for p in info.get("prerequisites", []) if p in ids]
        for sid, info in content.subtopics.items()
    }
    down: dict[str, list[str]] = {sid: [] for sid in ids}
    for sid, ps in up.items():
        for p in ps:
            down[p].append(sid)
    return up, down


def _closure(start: str, edges: dict[str, list[str]]) -> set[str]:
    seen: set[str] = set()
    todo = list(edges.get(start, []))
    while todo:
        n = todo.pop()
        if n not in seen:
            seen.add(n)
            todo.extend(edges.get(n, []))
    seen.discard(start)
    return seen


def _label(
    db: Session, content: ContentStore, ps: t.PlacementSession, subtopic_id: str, passed: bool
) -> None:
    """Graph inference (UI_SPEC 2.4 table): labels only, never a score. Subtopics that already
    have real evidence (a check result, a score, a finished lesson) are left alone."""
    up, down = _graph(content)
    targets = _closure(subtopic_id, up if passed else down)
    hint = "likely_known" if passed else "likely_gap"
    measured = set(
        db.scalars(
            select(t.CheckResult.subtopic_id).where(t.CheckResult.user_id == ps.user_id).distinct()
        )
    )
    for sid in targets:
        row = db.get(t.UserSubtopic, (ps.user_id, sid))
        if row is None or sid in measured or row.score > 0 or row.lesson_done_at is not None:
            continue
        if hint == "likely_gap" and row.placement_hint is not None:
            continue  # a known-by-inference ancestor of a passed gate is never turned into a gap
        row.placement_hint = hint
        row.placement_session_id = ps.id
    db.flush()


# ---- state machine ----


def _decided(g: dict[str, Any]) -> bool:
    return g["outcome"] is not None


def _sync_active(ps: t.PlacementSession, active_ms: int | None, now: datetime) -> None:
    """Active time is reported by the client as an absolute value (a resend is safe); it only goes
    up, and never faster than the wall clock since the session started."""
    if active_ms is not None:
        cap = int((now - ps.started_at).total_seconds() * 1000) + ACTIVE_SLACK_MS
        ps.active_ms = max(ps.active_ms, min(active_ms, cap))
    ps.last_active_at = now


def _stop(ps: t.PlacementSession, state: dict[str, Any], reason: str, now: datetime) -> None:
    ps.status = "finished"
    ps.stop_reason = reason
    ps.finished_at = now
    state["cursor"] = None
    state["probing"] = False


def _ask(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    idx: int,
    probing: bool,
    now: datetime,
    key: str | None,
) -> None:
    g = state["gates"][idx]
    if ps.active_ms + int(g["minutes"] * 60_000) > HARD_MS:
        _stop(ps, state, "budget", now)  # no new gate when it cannot finish inside the hard cap
        return
    item = checks.find_item(content, g["subtopic_id"], g["item_id"])
    cs = checks.begin_session(
        db,
        content,
        ps.user_id,
        g["subtopic_id"],
        "placement",
        2,
        now,
        key=key,
        item=item,
        placement_session_id=ps.id,
    )
    g["check_session_id"] = cs.id
    state["cursor"] = idx
    state["probing"] = probing


def _go_up(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    idx: int,
    now: datetime,
    key: str | None,
) -> None:
    gates = state["gates"]
    while True:
        if idx > state["last"]:
            _stop(ps, state, "entry_gates_done" if ps.experience == "none" else "all_gates", now)
            return
        g = gates[idx]
        if g["outcome"] is None:
            _ask(db, content, ps, state, idx, False, now, key)
            return
        if g["outcome"] in FAIL_LIKE:  # a preset "locked" gate: a real fail within 24 h
            _after_fail(db, content, ps, state, idx, now, key)
            return
        idx += 1  # unavailable / already known


def _after_fail(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    k: int,
    now: datetime,
    key: str | None,
) -> None:
    gates = state["gates"]
    if state["probing"]:
        return _stop(ps, state, "two_fails", now)
    if k == 0 or gates[k - 1]["outcome"] == "unavailable":
        return _stop(ps, state, "failed_start", now)  # nothing below: stop, no Phase B
    below = gates[k - 1]
    if below["outcome"] in PASS_LIKE:
        return _stop(ps, state, "fail_after_pass", now)
    if below["outcome"] in FAIL_LIKE:
        return _stop(ps, state, "two_fails", now)
    _ask(db, content, ps, state, k - 1, True, now, key)  # exactly one gate below


def _after_pass(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    k: int,
    now: datetime,
    key: str | None,
) -> None:
    if state["probing"]:
        return _stop(ps, state, "fail_after_pass", now)
    _go_up(db, content, ps, state, k + 1, now, key)


def _l2_result(cs: t.CheckSession) -> dict[str, Any] | None:
    return next(
        (s["result"] for s in cs.ladder["steps"] if s["level"] == 2 and s["result"] is not None),
        None,
    )


def _l1_label(cs: t.CheckSession) -> str | None:
    r = next((s["result"] for s in cs.ladder["steps"] if s["level"] == 1 and s["result"]), None)
    if r is None:
        return None
    return "gave_up" if r["gave_up"] else "passed" if r["passed"] else "failed"


def _close_gate(
    db: Session, content: ContentStore, ps: t.PlacementSession, state: dict[str, Any]
) -> str | None:
    """Fix the outcome of the current gate from its level-2 result and label the graph.
    Returns the outcome, or None when level 2 has not been answered."""
    g = state["gates"][state["cursor"]]
    cs = db.get(t.CheckSession, g["check_session_id"])
    assert cs is not None
    res = _l2_result(cs)
    if res is None:
        return None
    if res["gave_up"]:
        out = "gave_up"
    elif res["passed"]:
        out = "passed" if res["clean"] else "passed_unclean"
    else:
        out = "failed"
    g["outcome"] = out
    g["l1"] = _l1_label(cs)
    if out in FAIL_LIKE:
        state["fails"] += 1
    row = db.get(t.UserSubtopic, (ps.user_id, g["subtopic_id"]))
    if row is not None:
        row.placement_hint = None  # real evidence replaces any label
        row.placement_session_id = ps.id
        if g["l1"] == "passed" and out in FAIL_LIKE:
            row.known_basic = True  # only level 1 passed: "đã biết sơ", the score is untouched
    if out == "passed":
        _label(db, content, ps, g["subtopic_id"], True)
    elif out in FAIL_LIKE:
        _label(db, content, ps, g["subtopic_id"], False)
    db.flush()
    return out


def _settle(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    now: datetime,
    key: str | None,
) -> None:
    """The current gate has finished its ladder: decide the next gate or stop."""
    k = state["cursor"]
    out = _close_gate(db, content, ps, state)
    assert out is not None
    progress.record_event(
        db,
        "placement_gate_done",
        {"placement_id": ps.id, "gate": state["gates"][k]["code"], "outcome": out},
        now=now,
        idem_key=key,
    )
    if out in PASS_LIKE:
        _after_pass(db, content, ps, state, k, now, key)
    else:
        _after_fail(db, content, ps, state, k, now, key)


# ---- views ----


def _gate_session(db: Session, state: dict[str, Any]) -> t.CheckSession | None:
    if state.get("cursor") is None:
        return None
    g = state["gates"][state["cursor"]]
    return db.get(t.CheckSession, g["check_session_id"]) if g["check_session_id"] else None


def view(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    *,
    resumed: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    state = ps.state
    current = None
    cs = _gate_session(db, state)
    if ps.status == "in_progress" and cs is not None:
        step = checks._current_step(cs.ladder)
        g = state["gates"][state["cursor"]]
        current = {
            "gate": g["code"],
            "subtopic_id": g["subtopic_id"],
            "name_vi": g["name_vi"],
            "probing": state["probing"],
            "check_session_id": cs.id,
            "elapsed_ms": cs.elapsed_ms,
            "step": (
                {
                    "index": cs.ladder["steps"].index(step),
                    "count": len(cs.ladder["steps"]),
                    **checks.public_item(content, g["subtopic_id"], step),
                }
                if step
                else None
            ),
        }
    entry = state.get("entry", 0)
    in_scope = [
        g for g in state["gates"][entry : state["last"] + 1] if g["outcome"] != "unavailable"
    ]
    return {
        "placement_id": ps.id,
        "status": ps.status,
        "kind": ps.kind,
        "scope": ps.scope,
        "experience": ps.experience,
        "resumed": resumed,
        # no activity for 7 days: the UI offers continue / settle / start over (UI_SPEC 2.6)
        "stale": bool(
            now and ps.status == "in_progress" and now - ps.last_active_at >= STALE_AFTER
        ),
        "stop_reason": ps.stop_reason,
        "message_vi": MESSAGES.get(ps.stop_reason or ""),
        "started_at": _iso(ps.started_at),
        "last_active_at": _iso(ps.last_active_at),
        "finished_at": _iso(ps.finished_at),
        "active_ms": ps.active_ms,
        "budget": {
            "soft_ms": SOFT_MS,
            "hard_ms": HARD_MS,
            "remaining_ms": max(0, HARD_MS - ps.active_ms),
        },
        "progress": {
            "gates_total": len(in_scope),
            "gates_done": sum(1 for g in in_scope if _decided(g)),
        },
        "gates": [
            {k: g[k] for k in ("code", "subtopic_id", "name_vi", "outcome", "l1", "retry_after")}
            for g in state["gates"]
        ],
        "current": current,
    }


# ---- public API ----


def _own(db: Session, user_id: int, placement_id: int) -> t.PlacementSession:
    ps = db.get(t.PlacementSession, placement_id)
    if ps is None or ps.user_id != user_id:
        raise ApiError(404, "placement_not_found", f"No placement session {placement_id}")
    return ps


def active(db: Session, user_id: int) -> t.PlacementSession | None:
    return db.scalar(
        select(t.PlacementSession)
        .where(t.PlacementSession.user_id == user_id, t.PlacementSession.status == "in_progress")
        .order_by(t.PlacementSession.id.desc())
        .limit(1)
    )


def latest(db: Session, user_id: int) -> t.PlacementSession | None:
    return db.scalar(
        select(t.PlacementSession)
        .where(
            t.PlacementSession.user_id == user_id,
            t.PlacementSession.status.in_(("in_progress", "finished", "skipped")),
        )
        .order_by(t.PlacementSession.id.desc())
        .limit(1)
    )


def onboarding_state(db: Session, user_id: int, choice: str | None) -> str:
    """`GET /me.onboarding.placement`: none | in_progress | finished | skipped."""
    ps = latest(db, user_id)
    if ps is not None:
        return {"in_progress": "in_progress", "finished": "finished", "skipped": "skipped"}[
            ps.status
        ]
    return "skipped" if choice == "skipped" else "none"


def _ensure_gate(
    db: Session, content: ContentStore, ps: t.PlacementSession, now: datetime, key: str | None
) -> None:
    """A gate item idle for 24 h is `expired` (not a failure): reissue it, or, when its level 2 was
    already answered, take that result as the gate outcome."""
    state = copy.deepcopy(ps.state)
    cs = _gate_session(db, state)
    if cs is None or cs.status != "in_progress":
        return
    if now < cs.last_active_at + checks.SESSION_TTL:
        return
    cs.status = "expired"
    if _l2_result(cs) is not None:
        _settle(db, content, ps, state, now, key)
    else:
        _ask(db, content, ps, state, state["cursor"], state["probing"], now, key)
    ps.state = state
    db.flush()


def start(
    db: Session,
    content: ContentStore,
    user_id: int,
    now: datetime,
    *,
    experience: str | None = None,
    restart: bool = False,
    skip: bool = False,
    key: str | None = None,
) -> tuple[t.PlacementSession, bool]:
    """Begin a placement, or resume the one in progress. `skip` = "Bắt đầu từ đầu": a session row
    with status `skipped` and nothing else (no check_results, no events about scores)."""
    cur = active(db, user_id)
    if cur is not None and not restart and not skip:
        _ensure_gate(db, content, cur, now, key)
        cur.last_active_at = now
        db.flush()
        return cur, True
    if cur is not None:  # restart / skip: abandon the sitting; measured results stay evidence
        _abandon(db, cur, now)
    settings = db.get(t.UserSettings, user_id)
    exp = experience or (settings.experience if settings else None) or "none"
    if skip:
        ps = t.PlacementSession(
            user_id=user_id,
            status="skipped",
            experience=exp,
            state={"gates": [], "cursor": None, "probing": False, "fails": 0, "last": -1},
            active_ms=0,
            stop_reason="skipped",
            started_at=now,
            last_active_at=now,
            finished_at=now,
        )
        db.add(ps)
        if settings is not None:
            settings.placement_choice = "skipped"  # the A8 flag
        db.flush()
        return ps, False

    gates = _build_gates(db, content, user_id, now)
    state: dict[str, Any] = {
        "gates": gates,
        "entry": ENTRY[exp],
        "last": LAST_GATE[exp],
        "cursor": None,
        "probing": False,
        "fails": 0,
    }
    ps = t.PlacementSession(
        user_id=user_id,
        kind="initial",
        scope="all",
        status="in_progress",
        experience=exp,
        state=state,
        active_ms=0,
        started_at=now,
        last_active_at=now,
    )
    db.add(ps)
    db.flush()
    progress.record_event(
        db,
        "placement_started",
        {"placement_id": ps.id, "experience": exp},
        now=now,
        idem_key=key,
    )
    state = copy.deepcopy(state)
    if not any(g["outcome"] != "unavailable" for g in gates):
        _stop(ps, state, "no_gates", now)
    else:
        _go_up(db, content, ps, state, state["entry"], now, key)
    ps.state = state  # reassign: SQLAlchemy does not track in-place JSON changes
    if ps.status == "finished":
        progress.record_event(
            db,
            "placement_finished",
            {"placement_id": ps.id, "reason": ps.stop_reason},
            now=now,
            idem_key=key,
        )
    db.flush()
    return ps, False


def _abandon(db: Session, ps: t.PlacementSession, now: datetime) -> None:
    cs = _gate_session(db, ps.state)
    if cs is not None and cs.status == "in_progress":
        cs.status = "expired"
    ps.status = "abandoned"
    ps.stop_reason = "restarted"
    ps.finished_at = now
    db.flush()


def get(
    db: Session, content: ContentStore, user_id: int, placement_id: int, now: datetime
) -> dict[str, Any]:
    ps = _own(db, user_id, placement_id)
    return view(db, content, ps, now=now)


def heartbeat(
    db: Session,
    content: ContentStore,
    user_id: int,
    placement_id: int,
    active_ms: int,
    item_elapsed_ms: int | None,
    now: datetime,
) -> dict[str, Any]:
    ps = _own(db, user_id, placement_id)
    if ps.status == "in_progress":
        _sync_active(ps, active_ms, now)
        cs = _gate_session(db, ps.state)
        if cs is not None and cs.status == "in_progress":
            if item_elapsed_ms is not None:
                cs.elapsed_ms = max(cs.elapsed_ms or 0, item_elapsed_ms)
            cs.last_active_at = now
        db.flush()
    return {
        "placement_id": ps.id,
        "status": ps.status,
        "active_ms": ps.active_ms,
        "budget": {
            "soft_ms": SOFT_MS,
            "hard_ms": HARD_MS,
            "remaining_ms": max(0, HARD_MS - ps.active_ms),
        },
        "item_elapsed_ms": (cs.elapsed_ms if ps.status == "in_progress" and cs else None),
    }


def answer(
    db: Session,
    content: ContentStore,
    user_id: int,
    placement_id: int,
    body: Any,
    now: datetime,
    *,
    key: str | None = None,
) -> dict[str, Any]:
    """Grade the current item (`body.gave_up` = "Không biết"), then move the ladder on."""
    ps = _own(db, user_id, placement_id)
    if ps.status != "in_progress":
        raise ApiError(409, "placement_finished", "This placement is already finished")
    state = copy.deepcopy(ps.state)
    cs = _gate_session(db, state)
    assert cs is not None
    if cs.status == "in_progress" and now >= cs.last_active_at + checks.SESSION_TTL:
        _ensure_gate(db, content, ps, now, key)  # reissue, then ask the client to reload
        raise ApiError(409, "placement_item_expired", "This item expired; reload the placement")
    g = state["gates"][state["cursor"]]
    _sync_active(ps, body.session_elapsed_ms, now)
    out = checks.answer(
        db,
        content,
        user_id,
        g["subtopic_id"],
        SimpleNamespace(**{**body.model_dump(), "session_id": cs.id, "session_elapsed_ms": None}),
        now,
        key=key,
    )
    db.refresh(cs)
    if cs.status == "done":
        _settle(db, content, ps, state, now, key)
    else:  # level 1 is next in the same gate
        row = db.get(t.UserSubtopic, (user_id, g["subtopic_id"]))
        if row is not None:
            row.placement_session_id = ps.id
    ps.state = state
    if ps.status == "finished":
        progress.record_event(
            db,
            "placement_finished",
            {"placement_id": ps.id, "reason": ps.stop_reason},
            now=now,
            idem_key=key,
        )
    db.flush()
    return {
        "result": out["result"],
        "score": out["score"],
        "gate_outcome": next(
            (x["outcome"] for x in state["gates"] if x["check_session_id"] == cs.id), None
        ),
        "placement": view(db, content, ps),
    }


def finish(
    db: Session,
    content: ContentStore,
    user_id: int,
    placement_id: int,
    active_ms: int | None,
    now: datetime,
    *,
    key: str | None = None,
) -> dict[str, Any]:
    """ "Kết thúc sớm" / "Dừng và lưu": keep what was measured; the open item is dropped without a
    failure (an unanswered item writes nothing)."""
    ps = _own(db, user_id, placement_id)
    if ps.status == "in_progress":
        state = copy.deepcopy(ps.state)
        _sync_active(ps, active_ms, now)
        cs = _gate_session(db, state)
        if cs is not None and cs.status == "in_progress":
            _close_gate(db, content, ps, state)  # labels only if its level 2 was answered
            cs.status = "expired"
        _stop(ps, state, "user_finished", now)
        ps.state = state
        progress.record_event(
            db,
            "placement_finished",
            {"placement_id": ps.id, "reason": "user_finished"},
            now=now,
            idem_key=key,
        )
        db.flush()
    return view(db, content, ps)


def result(db: Session, content: ContentStore, user_id: int, placement_id: int) -> dict[str, Any]:
    """Reduced result: seeded skill map, strong/weak areas, where to start (UI_SPEC S3)."""
    ps = _own(db, user_id, placement_id)
    gates = ps.state["gates"]
    rows = {
        r.subtopic_id: r
        for r in db.scalars(select(t.UserSubtopic).where(t.UserSubtopic.user_id == user_id))
    }
    seeded = {g["subtopic_id"] for g in gates if g["outcome"] == "passed"}
    measured_ids = {
        g["subtopic_id"] for g in gates if g["outcome"] not in (None, "unavailable", "locked")
    }
    skill_map = []
    for sid in content.ordered_subtopic_ids():
        row = rows.get(sid)
        hint = row.placement_hint if row else None
        measured = sid in measured_ids
        skill_map.append(
            {
                "subtopic_id": sid,
                "name_vi": content.subtopics[sid]["name_vi"],
                "score": row.score if row else 0,
                "state": "measured" if measured else (hint or "not_assessed"),
                "seeded": sid in seeded,
                "known_basic": bool(row and row.known_basic),
                "placement_hint": hint,
            }
        )
    strong = [
        {"gate": g["code"], "name_vi": g["name_vi"], "subtopic_id": g["subtopic_id"]}
        for g in gates
        if g["outcome"] in ("passed", "passed_unclean", "known")
    ]
    weak = [
        {
            "gate": g["code"],
            "name_vi": g["name_vi"],
            "subtopic_id": g["subtopic_id"],
            "outcome": g["outcome"],
            "retry_after": g["retry_after"],
        }
        for g in gates
        if g["outcome"] in FAIL_LIKE
    ]
    start_at = None
    for sid in content.ordered_subtopic_ids():
        row = rows.get(sid)
        if content.lesson(sid) is None or (row and row.score >= 2):
            continue
        if row and row.placement_hint == "likely_known":
            continue  # offered as "Test out" instead
        start_at = {"subtopic_id": sid, "name_vi": content.subtopics[sid]["name_vi"]}
        break
    pending = [
        sid
        for sid in content.ordered_subtopic_ids()
        if content.lesson(sid) is not None
        and rows.get(sid) is not None
        and rows[sid].placement_hint == "likely_known"
        and rows[sid].score < 2
    ]
    return {
        "placement_id": ps.id,
        "status": ps.status,
        "stop_reason": ps.stop_reason,
        "message_vi": MESSAGES.get(ps.stop_reason or ""),
        "active_ms": ps.active_ms,
        "seeded": sorted(seeded),
        "skill_map": skill_map,
        "strong_areas": strong,
        "weak_areas": weak,
        "start": start_at,
        # no published lesson left to start from: S3 says "content is being written" and offers
        # Test out for the likely_known ones that do have a lesson
        "content_pending": start_at is None,
        "test_out_candidates": pending,
        "counts": {
            "measured": sum(1 for m in skill_map if m["state"] == "measured"),
            "likely_known": sum(1 for m in skill_map if m["state"] == "likely_known"),
            "likely_gap": sum(1 for m in skill_map if m["state"] == "likely_gap"),
            "not_assessed": sum(1 for m in skill_map if m["state"] == "not_assessed"),
        },
    }
