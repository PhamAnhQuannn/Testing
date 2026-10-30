"""Placement, Phase A (SPEC 5.6, UI_SPEC 2): the gate ladder C1-C7 climbed in RUNGS (leveled).

Placement is a mastery check ordered by the prerequisite graph. It writes ONLY `check_results`
(context=placement) through the same `checks.answer` flow; the score is recomputed from events by
`scoring.py`. Each gate climbs up to three rungs of increasing type difficulty, one item each:

- P0 knowledge: an `mcq` item (level 1, ~1 min, keyed on the server);
- P1 trace: a `read_code` item (level 1, ~2 min, "what does this print?", string compare);
- P2 code: the gate's level-2 `write_code` item (6-9 min, graded by the browser tests).

P0/P1 items come from the separate placement pool (`content.placement`, never mixed into the
mastery checks). A gate without P0/P1 authored runs P2 only (the Phase A behaviour). Scoring: a
clean P2 pass is `tested_out` (2); a clean keyed P0/P1 pass is `tested_basic` (1); a self-graded
`concept` item is never asked here. Level 3 is never asked. Graph inference is a label
(`user_subtopic.placement_hint`) and never a score. "Start from scratch" writes nothing.

Branching per gate: P0 fail/give-up = `knowledge_gap` (no P1/P2; the gate one below gets its P0
only, then stop); P0 pass -> P1; P1 fail/give-up stops the gate with `known_basic` set (skip P2;
the gate one below gets its P2 as a probe, then stop); P1 pass -> P2; a P2 pass goes up to the next
gate (starting at its P0); a P2 fail probes the gate one below (its P2) and stops. `experience`
picks the entry gate (none -> C1, some -> C2, solid -> C3); `none` only ever runs C1 -> C2. A failed
gate stops the run once the gate right below it has been tried, or at once when there is none.
The one-sitting budget is 45 min soft / 60 min hard of ACTIVE time (client heartbeats, absolute and
monotonic); Phase A uses the hard one: no new rung when active + its cost > 60 min.
(Changed by PR: placement leveled rungs.)

CONCEPT phase (System Design + AI-engineer tracks, no code): when the code ladder stops, a track
with authored module hubs enters `phase = "concept_offer"`; the user self-reports which modules
they know (`select_modules`), and each selected module becomes a 2-rung `kind = "concept"` gate on
its HUB subtopic, appended to the same `state["gates"]` list: C1 = a level-1 `mcq` (clean pass =
score 1 via tested_basic), C2 = a level-2 `mcq` (keyed; clean pass = tested_out = score 2, the
approved concept-path evidence). C2 needs a C1 pass first. Concept gates never go up or probe
below; graph inference is a display-only label as everywhere else.
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


def _gate(code: str, sid: str, name: str, p0: str | None, p1: str | None, p2: str) -> dict:
    return {
        "code": code,
        "kind": "code",
        "subtopic_id": sid,
        "name_vi": name,
        "p0": p0,
        "p1": p1,
        "p2": p2,
    }


# In difficulty order (UI_SPEC 2.2, assessment clusters). p0 = mcq, p1 = read_code (both from
# content/placement), p2 = the gate's level-2 write_code item. p0/p1 None = that rung is not
# authored yet: the gate skips it (every gate C1-C7 now has both).
GATES: list[dict[str, Any]] = [
    _gate("C1", "py.core.strings", "Python căn bản", "P900", "P903", "Q012"),
    _gate(
        "C2", "py.datastructs.dict", "Cấu trúc dữ liệu Python, hàm, Big-O", "P910", "P913", "Q023"
    ),
    _gate(
        "C3",
        "dsa.arrays_strings.hash_tables",
        "Mảng, chuỗi, hash, prefix sum",
        "P915",
        "P918",
        "Q258",
    ),
    _gate(
        "C4",
        "dsa.two_pointers_window.two_pointers",
        "Hai con trỏ, cửa sổ trượt",
        "P920",
        "P923",
        "Q070",
    ),
    _gate(
        "C5", "dsa.linked_list.ll_basics", "Class, linked list, stack/queue", "P925", "P928", "Q079"
    ),
    _gate(
        "C6",
        "dsa.searching_sorting.binary_search_basics",
        "Binary search, sorting",
        "P930",
        "P933",
        "Q095",
    ),
    _gate("C7", "dsa.trees.tree_basics", "Cây, heap, design, intervals", "P935", "P938", "Q105"),
]
# Concept hubs per profile track: (module_id, hub_subtopic_id, name_vi), in tree order. A module is
# only OFFERED when its hub has both a level-1 and a level-2 mcq in content/placement.
CONCEPT_HUBS: dict[str, list[tuple[str, str, str]]] = {
    "swe": [
        ("sd.fundamentals", "sd.fundamentals.scalability", "Nền tảng thiết kế hệ thống"),
        ("sd.framework", "sd.framework.overview", "Khung phỏng vấn system design"),
        ("sd.data", "sd.data.sql_vs_nosql", "Lưu trữ và mô hình dữ liệu"),
        ("sd.caching", "sd.caching.patterns", "Caching"),
        ("sd.networking", "sd.networking.load_balancing", "Mạng và load balancing"),
        ("sd.api", "sd.api.api_styles", "Thiết kế API"),
        ("sd.async", "sd.async.queues_pubsub", "Xử lý bất đồng bộ (queue, pub/sub)"),
        ("sd.distributed", "sd.distributed.failures_model", "Hệ phân tán"),
        ("sd.technologies", "sd.technologies.stores", "Công nghệ lưu trữ thực tế"),
        ("sd.reliability_ops", "sd.reliability_ops.fault_tolerance", "Độ tin cậy và vận hành"),
    ],
    "ai": [
        ("ml.llm", "ml.llm.llm_basics_pretraining", "LLM căn bản"),
        ("ml.rag_agents", "ml.rag_agents.rag_pipeline", "RAG và agent"),
        (
            "ml.llm_eval_serving",
            "ml.llm_eval_serving.eval_sets_metrics",
            "Đánh giá và serving LLM",
        ),
        ("ml.system_design", "ml.system_design.framework", "Thiết kế hệ thống ML"),
    ],
}
MAX_CONCEPT_GATES = 4
CONCEPT_MINUTES = (1, 0, 2)  # C1 mcq, (no middle rung), C2 mcq
RUNG_KIND = ("mcq", "read_code", "write_code")  # P0, P1, P2
DEFAULT_MINUTES = (1, 2, 6)
ENTRY = {"none": 0, "some": 1, "solid": 2}
LAST_GATE = {"none": 1, "some": 6, "solid": 6}  # `none` only runs C1 -> C2 (UI_SPEC 2.4 A1)

PASS_LIKE = {"passed", "passed_unclean", "known", "known_basic"}
FAIL_LIKE = {"failed", "gave_up", "locked", "knowledge_gap"}

MESSAGES = {
    "failed_start": "Chưa cần đo thêm; bắt đầu từ nền tảng sẽ hiệu quả hơn.",
    "two_fails": "Chưa cần đo thêm; bắt đầu từ nền tảng sẽ hiệu quả hơn.",
    "fail_after_pass": "Đã tìm được ranh giới trình độ của bạn.",
    "all_gates": "Bạn đã qua tất cả các cổng đánh giá.",
    "entry_gates_done": "Đã đo xong phần nền tảng.",
    "budget": "Đã hết thời gian đánh giá của lần này.",
    "user_finished": "Bạn đã kết thúc sớm; kết quả đã đo được giữ lại.",
    "no_gates": "Chưa có cổng đánh giá nào sẵn sàng.",
    "concept_done": "Đã đo xong các module khái niệm bạn chọn.",
    "concept_skipped": "Bạn đã bỏ qua phần đo module khái niệm.",
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


def _rung_item(
    content: ContentStore, sid: str, item_id: str | None, rung: int
) -> dict[str, Any] | None:
    """A P0/P1 item of the placement pool (level 1, the right type), else None (rung skipped)."""
    if not item_id:
        return None
    it = content.find_check_item(sid, item_id)
    if it is None or it["type"] != RUNG_KIND[rung] or it.get("difficulty") != 1:
        return None
    return it


def _build_gates(
    db: Session, content: ContentStore, user_id: int, now: datetime
) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for spec in GATES:
        sid = spec["subtopic_id"]
        g: dict[str, Any] = {
            "code": spec["code"],
            "subtopic_id": sid,
            "name_vi": spec["name_vi"],
            "rung_items": [None, None, None],  # item id per rung P0 / P1 / P2
            "rung_minutes": list(DEFAULT_MINUTES),
            "rung": None,  # the rung currently asked (0 / 1 / 2)
            "rung_results": {},  # "0"/"1"/"2" -> passed | failed | gave_up
            "outcome": None,
            "check_session_id": None,
            "kind": "code",
            "l1": None,  # label of the last knowledge rung (P0/P1) that was answered
            "retry_after": None,
        }
        item = _gate_item(content, sid, spec["p2"]) if sid in content.subtopics else None
        if item is None:
            g["outcome"] = "unavailable"  # not placeable (no level-2 write_code check problem)
        else:
            g["rung_items"][2] = item["id"]
            g["rung_minutes"][2] = item.get("minutes") or 8
            for r, key in ((0, "p0"), (1, "p1")):
                rung_item = _rung_item(content, sid, spec[key], r)
                if rung_item is not None:
                    g["rung_items"][r] = rung_item["id"]
                    g["rung_minutes"][r] = rung_item.get("minutes") or DEFAULT_MINUTES[r]
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
    state["phase"] = "finished"


def _is_concept(g: dict[str, Any]) -> bool:
    return g.get("kind", "code") == "concept"


def _concept_item(content: ContentStore, hub: str, level: int) -> dict[str, Any] | None:
    """The hub's keyed mcq of this difficulty from the placement pool (first one authored)."""
    return next(
        (
            i
            for i in content.placement.get(hub, [])
            if i["type"] == "mcq" and i.get("difficulty") == level
        ),
        None,
    )


def concept_offer(content: ContentStore, track: str | None) -> list[dict[str, Any]]:
    """The track's modules whose hub is authored (a level-1 AND a level-2 mcq): offered to the
    user's self-report. Modules without content yet are silently absent."""
    out = []
    for module, hub, name in CONCEPT_HUBS.get(track or "", []):
        if hub not in content.subtopics:
            continue
        c1, c2 = _concept_item(content, hub, 1), _concept_item(content, hub, 2)
        if c1 is None or c2 is None:
            continue
        out.append(
            {
                "module": module,
                "name_vi": name,
                "hub_subtopic_id": hub,
                "minutes": [c1.get("minutes") or 1, c2.get("minutes") or 2],
            }
        )
    return out


def _track(db: Session, user_id: int) -> str | None:
    settings = db.get(t.UserSettings, user_id)
    return settings.track if settings else None


def _end_code_phase(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    reason: str,
    now: datetime,
) -> None:
    """The code ladder reached a terminal stop. If the user's track has authored concept hubs and
    a C1 still fits the hard budget, wait for the module self-report; else finish for real."""
    offer = concept_offer(content, _track(db, ps.user_id))
    if (
        state.get("phase", "code") == "code"
        and offer
        and ps.active_ms + int(min(o["minutes"][0] for o in offer) * 60_000) <= HARD_MS
    ):
        state["phase"] = "concept_offer"
        state["code_stop_reason"] = reason
        state["cursor"] = None
        state["probing"] = False
        return
    _stop(ps, state, reason, now)


def _first_rung(g: dict[str, Any]) -> int:
    """The lowest authored rung of a gate (P2 when no P0/P1 is authored)."""
    return next((r for r in (0, 1) if g["rung_items"][r]), 2)


def _next_rung(g: dict[str, Any], rung: int) -> int:
    return next((r for r in range(rung + 1, 2) if g["rung_items"][r]), 2)


def _ask(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    idx: int,
    probing: bool,
    now: datetime,
    key: str | None,
    rung: int | None = None,
) -> None:
    """Open the session of one rung of gate `idx` (default: its lowest authored rung)."""
    g = state["gates"][idx]
    r = _first_rung(g) if rung is None else rung
    if ps.active_ms + int(g["rung_minutes"][r] * 60_000) > HARD_MS:
        # no new rung when it cannot finish inside the hard cap
        if _is_concept(g):
            _stop(ps, state, "budget", now)
        else:
            _end_code_phase(db, content, ps, state, "budget", now)
        return
    item = checks.find_item(content, g["subtopic_id"], g["rung_items"][r])
    cs = checks.begin_session(
        db,
        content,
        ps.user_id,
        g["subtopic_id"],
        "placement",
        2 if r == 2 else 1,
        now,
        key=key,
        item=item,
        placement_session_id=ps.id,
    )
    g["check_session_id"] = cs.id
    g["rung"] = r
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
            reason = "entry_gates_done" if ps.experience == "none" else "all_gates"
            _end_code_phase(db, content, ps, state, reason, now)
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
    *,
    knowledge_only: bool = False,
) -> None:
    """Probe exactly one gate below, or stop. After a P0 failure (`knowledge_only`) the probe is
    the lower gate's P0 only (when it has one); after any other failure it is its P2."""
    gates = state["gates"]
    if state["probing"]:
        return _end_code_phase(db, content, ps, state, "two_fails", now)
    if k == 0 or gates[k - 1]["outcome"] == "unavailable":
        return _end_code_phase(db, content, ps, state, "failed_start", now)  # nothing below
    below = gates[k - 1]
    if below["outcome"] in PASS_LIKE:
        return _end_code_phase(db, content, ps, state, "fail_after_pass", now)
    if below["outcome"] in FAIL_LIKE:
        return _end_code_phase(db, content, ps, state, "two_fails", now)
    rung = 0 if knowledge_only and below["rung_items"][0] else 2
    _ask(db, content, ps, state, k - 1, True, now, key, rung)  # exactly one gate below


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
        return _end_code_phase(db, content, ps, state, "fail_after_pass", now)
    _go_up(db, content, ps, state, k + 1, now, key)


def _rung_result(cs: t.CheckSession) -> dict[str, Any] | None:
    """The result of the (single) item a rung session asks."""
    return next((s["result"] for s in cs.ladder["steps"] if s["result"] is not None), None)


def _label_of(res: dict[str, Any]) -> str:
    return "gave_up" if res["gave_up"] else "passed" if res["passed"] else "failed"


def _close_gate(
    db: Session, content: ContentStore, ps: t.PlacementSession, state: dict[str, Any]
) -> tuple[str | None, str | None]:
    """Record the result of the current rung. Returns (rung label, gate outcome): the label is None
    when the rung was not answered; the outcome is None while the gate still has rungs to climb
    (a clean P0/P1 pass). Labels the graph and flags `known_basic` as evidence comes in."""
    g = state["gates"][state["cursor"]]
    cs = db.get(t.CheckSession, g["check_session_id"])
    assert cs is not None
    res = _rung_result(cs)
    if res is None:
        return None, None
    rung, label = g["rung"], _label_of(res)
    g["rung_results"][str(rung)] = label
    if _is_concept(g):
        return label, _close_concept(db, content, ps, g, rung, label, res)
    if rung < 2:
        g["l1"] = label
    row = db.get(t.UserSubtopic, (ps.user_id, g["subtopic_id"]))
    keyed_pass = any(g["rung_results"].get(k) == "passed" for k in ("0", "1"))
    if rung == 2:
        out = "gave_up" if label == "gave_up" else "failed" if label == "failed" else None
        out = out or ("passed" if res["clean"] else "passed_unclean")
    elif label == "passed":
        out = "known_basic" if state["probing"] else None  # a probe never climbs further
    elif keyed_pass:  # P1 failed after a P0 pass: knows the basics, cannot trace code
        out = label
    else:
        out = "knowledge_gap"  # the first knowledge rung failed / was given up
    if row is not None:
        if label == "passed" or out is not None:
            row.placement_hint = None  # real evidence replaces any label
            row.placement_session_id = ps.id
        if out is not None:
            # Set once the gate is decided: True when only P0/P1 passed ("đã biết sơ", score 1
            # via tested_basic), False when P2 cleanly tested out (score 2) so the flag never
            # lingers over a fully-known subtopic.
            row.known_basic = keyed_pass and out not in ("passed", "passed_unclean")
    if out is None:
        db.flush()
        return label, None
    g["outcome"] = out
    if out == "passed":
        _label(db, content, ps, g["subtopic_id"], True)
    elif out in FAIL_LIKE:
        _label(db, content, ps, g["subtopic_id"], False)
    db.flush()
    return label, out


def _close_concept(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    g: dict[str, Any],
    rung: int,
    label: str,
    res: dict[str, Any],
) -> str | None:
    """Decide a concept gate after a rung. C1 (rung 0) pass -> None (go on to C2); C1 fail / skip
    -> `knowledge_gap` (hub descendants labelled `likely_gap`); C2 (rung 2) pass -> `passed` (clean)
    or `passed_unclean`, hub ancestors labelled `likely_known`; a C2 fail keeps C1's basic flag."""
    row = db.get(t.UserSubtopic, (ps.user_id, g["subtopic_id"]))
    keyed_pass = g["rung_results"].get("0") == "passed"
    out: str | None
    if rung == 2:
        out = ("passed" if res["clean"] else "passed_unclean") if label == "passed" else label
    elif label == "passed":
        out = None
    else:
        out = "knowledge_gap"
    if row is not None:
        if label == "passed" or out is not None:
            row.placement_hint = None
            row.placement_session_id = ps.id
        if out is not None:
            row.known_basic = keyed_pass and out not in ("passed", "passed_unclean")
    if out is None:
        db.flush()
        return None
    g["outcome"] = out
    if out == "passed":
        _label(db, content, ps, g["subtopic_id"], True)
    elif out == "knowledge_gap":
        _label(db, content, ps, g["subtopic_id"], False)
    db.flush()
    return out


def _settle_concept(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    now: datetime,
    key: str | None,
) -> None:
    """A concept rung was answered: climb C1 -> C2 on a pass, else the gate is decided and the next
    concept gate starts (no go-up, no probe below); none left = `concept_done`."""
    k = state["cursor"]
    g = state["gates"][k]
    rung = g["rung"]
    label, out = _close_gate(db, content, ps, state)
    assert label is not None
    if out is None:
        _ask(db, content, ps, state, k, False, now, key, _next_rung(g, rung))
        return
    progress.record_event(
        db,
        "placement_gate_done",
        {"placement_id": ps.id, "gate": g["code"], "outcome": out},
        now=now,
        idem_key=key,
    )
    _start_next_concept(db, content, ps, state, k + 1, now, key)


def _start_next_concept(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    idx: int,
    now: datetime,
    key: str | None,
) -> None:
    gates = state["gates"]
    while idx < len(gates):
        if _is_concept(gates[idx]) and gates[idx]["outcome"] is None:
            _ask(db, content, ps, state, idx, False, now, key)
            return
        idx += 1
    _stop(ps, state, "concept_done", now)


def _settle(
    db: Session,
    content: ContentStore,
    ps: t.PlacementSession,
    state: dict[str, Any],
    now: datetime,
    key: str | None,
) -> None:
    """The current rung has been answered: climb to the next rung, or the gate is decided and we
    go up / probe below / stop."""
    if _is_concept(state["gates"][state["cursor"]]):
        return _settle_concept(db, content, ps, state, now, key)
    k = state["cursor"]
    g = state["gates"][k]
    rung = g["rung"]
    label, out = _close_gate(db, content, ps, state)
    assert label is not None
    if out is None:  # a clean pass below P2: the next rung of the same gate
        _ask(db, content, ps, state, k, False, now, key, _next_rung(g, rung))
        return
    progress.record_event(
        db,
        "placement_gate_done",
        {"placement_id": ps.id, "gate": g["code"], "outcome": out},
        now=now,
        idem_key=key,
    )
    if out in PASS_LIKE:
        _after_pass(db, content, ps, state, k, now, key)
    else:
        _after_fail(db, content, ps, state, k, now, key, knowledge_only=out == "knowledge_gap")


# ---- views ----


def _gate_session(db: Session, state: dict[str, Any]) -> t.CheckSession | None:
    if state.get("cursor") is None:
        return None
    g = state["gates"][state["cursor"]]
    return db.get(t.CheckSession, g["check_session_id"]) if g["check_session_id"] else None


def _with_defaults(g: dict[str, Any]) -> dict[str, Any]:
    """Sessions stored before the concept phase have no `kind` / `module` on their gates."""
    return {"kind": "code", "module": None, **g}


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
            "kind": g.get("kind", "code"),
            "module": g.get("module"),
            "probing": state["probing"],
            "rung": g["rung"],
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
    phase = state.get("phase", "code")
    offer = None
    if ps.status == "in_progress" and phase == "concept_offer":
        offer = [
            {k: o[k] for k in ("module", "name_vi", "hub_subtopic_id")}
            for o in concept_offer(content, _track(db, ps.user_id))
        ]
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
        "phase": phase,
        "awaiting_modules": offer is not None,  # UI shows the module self-report checklist
        "concept_offer": offer,
        "code_stop_reason": state.get("code_stop_reason"),
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
            {
                k: g[k]
                for k in (
                    "code",
                    "kind",
                    "module",
                    "subtopic_id",
                    "name_vi",
                    "outcome",
                    "l1",
                    "retry_after",
                    "rung_results",
                )
            }
            for g in (_with_defaults(x) for x in state["gates"])
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
    """A rung item idle for 24 h is `expired` (not a failure): reissue it, or, when it was already
    answered, take that result and move on."""
    state = copy.deepcopy(ps.state)
    cs = _gate_session(db, state)
    if cs is None or cs.status != "in_progress":
        return
    if now < cs.last_active_at + checks.SESSION_TTL:
        return
    cs.status = "expired"
    if _rung_result(cs) is not None:
        _settle(db, content, ps, state, now, key)
    else:
        g = state["gates"][state["cursor"]]
        _ask(db, content, ps, state, state["cursor"], state["probing"], now, key, g["rung"])
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
            state={"gates": [], "cursor": None, "probing": False, "last": -1},
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
        "phase": "code",
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
    if state.get("phase", "code") == "concept_offer":
        raise ApiError(409, "placement_awaiting_modules", "Choose the concept modules first")
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
    else:  # not finished (cannot happen: a rung is one item); keep the session marked
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


def select_modules(
    db: Session,
    content: ContentStore,
    user_id: int,
    placement_id: int,
    selected: list[str],
    active_ms: int | None,
    now: datetime,
    *,
    key: str | None = None,
) -> dict[str, Any]:
    """The module self-report: build one concept gate per selected module (offered ones only, tree
    order, at most MAX_CONCEPT_GATES) and start the first. An empty selection ends the sitting."""
    ps = _own(db, user_id, placement_id)
    if ps.status != "in_progress":
        raise ApiError(409, "placement_finished", "This placement is already finished")
    state = copy.deepcopy(ps.state)
    if state.get("phase", "code") != "concept_offer":
        raise ApiError(409, "placement_not_awaiting_modules", "No module selection is pending")
    track = _track(db, user_id)
    known = {m for m, _, _ in CONCEPT_HUBS.get(track or "", [])}
    unknown = sorted(set(selected) - known)
    if unknown:
        raise ApiError(422, "unknown_module", f"Not a module of this track: {', '.join(unknown)}")
    _sync_active(ps, active_ms, now)
    offered = {o["module"]: o for o in concept_offer(content, track)}
    picked = [
        (m, hub, name)
        for m, hub, name in CONCEPT_HUBS.get(track or "", [])
        if m in selected and m in offered
    ][:MAX_CONCEPT_GATES]
    if not picked:
        _stop(ps, state, state.get("code_stop_reason") or "concept_skipped", now)
    else:
        for n, (module, hub, name) in enumerate(picked, start=1):
            c1, c2 = _concept_item(content, hub, 1), _concept_item(content, hub, 2)
            assert c1 is not None and c2 is not None  # guaranteed by concept_offer
            state["gates"].append(
                {
                    "code": f"K{n}",
                    "kind": "concept",
                    "subtopic_id": hub,
                    "module": module,
                    "name_vi": name,
                    "rung_items": [c1["id"], None, c2["id"]],
                    "rung_minutes": [
                        c1.get("minutes") or CONCEPT_MINUTES[0],
                        0,
                        c2.get("minutes") or CONCEPT_MINUTES[2],
                    ],
                    "rung": None,
                    "rung_results": {},
                    "outcome": None,
                    "check_session_id": None,
                    "l1": None,
                    "retry_after": None,
                }
            )
        state["phase"] = "concept"
        _start_next_concept(db, content, ps, state, len(state["gates"]) - len(picked), now, key)
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
    return view(db, content, ps, now=now)


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
            _close_gate(db, content, ps, state)  # records evidence only if it was answered
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
    concept = [
        {
            "gate": g["code"],
            "module": g.get("module"),
            "name_vi": g["name_vi"],
            "subtopic_id": g["subtopic_id"],
            "outcome": g["outcome"],
            "score": rows[g["subtopic_id"]].score if g["subtopic_id"] in rows else 0,
        }
        for g in gates
        if _is_concept(g)
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
        "concept": concept,
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
