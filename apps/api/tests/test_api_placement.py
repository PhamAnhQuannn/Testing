"""Placement Phase A (A10): gate ladder + rungs, stop rules, budget, seeding (SPEC 5.6).

Tests named `test_rung_*` run on content where C1 and C2 also have a placement pool (P0 mcq, P1
read_code); tests named `test_concept_*` add concept hubs (System Design + AI) with C1/C2 mcqs;
every other test runs gates P2-only (the graceful fallback).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from sqlalchemy import select

from app.models import tables as t
from app.services import placement as pl
from app.services import progress
from app.services import scoring as sc
from app.services.content_loader import ContentStore

REPO_CONTENT = Path(__file__).resolve().parents[3] / "content"

# the seven gate subtopics form a prerequisite chain, like the real graph
CHAIN = [g["subtopic_id"] for g in pl.GATES]
GATE_ITEM = {g["subtopic_id"]: g["p2"] for g in pl.GATES}
EXTRA = "py.core.getting_started"  # prerequisite of C1, with a published lesson, no check items
SIDE = "py.core.loops"  # a descendant of C1 only (not a gate, no check items)


def _sub(sid: str, order: int, prereqs: list[str]) -> dict:
    return {
        "id": sid,
        "section": sid.split(".")[0],
        "module": ".".join(sid.split(".")[:2]),
        "name_vi": f"Mục {sid}",
        "order": order,
        "summary_vi": "tóm tắt",
        "mastery_bar_vi": "mức 3",
        "prerequisites": prereqs,
        "target_swe": {"intern": 2, "fresher": 3},
        "target_ai": {"intern": 2, "fresher": 3},
        "est_hours": 1.0,
        "plan_order": order,
    }


# concept hubs of the synthetic content: sid -> (prerequisites, has C1 mcq, has C2 mcq)
CONCEPT_SUBS = {
    "sd.data.intro": ([], False, False),
    "sd.data.sql_vs_nosql": (["sd.data.intro"], True, True),
    "sd.caching.patterns": (["sd.data.sql_vs_nosql"], True, True),
    "sd.caching.eviction_invalidation": (["sd.caching.patterns"], False, False),
    "sd.api.api_styles": ([], True, False),  # no level-2 mcq: not offered
    "sd.networking.load_balancing": ([], False, False),  # nothing authored: not offered
    "ml.rag_agents.rag_pipeline": ([], True, True),
}
HUB_DATA, HUB_CACHE = "sd.data.sql_vs_nosql", "sd.caching.patterns"


def build_placement_content(root: Path, rungs: bool = False, concept: bool = False) -> Path:
    (root / "index").mkdir(parents=True)
    subs = [_sub(EXTRA, 1, [])]
    prev = EXTRA
    for i, sid in enumerate(CHAIN):
        subs.append(_sub(sid, i + 2, [prev]))
        prev = sid
    subs.append(_sub(SIDE, 20, [CHAIN[0]]))
    if concept:
        for n, (sid, (prereqs, _c1, _c2)) in enumerate(CONCEPT_SUBS.items()):
            subs.append(_sub(sid, 30 + n, prereqs))
    (root / "index" / "subtopics.json").write_text(json.dumps({"subtopics": subs}))
    (root / "index" / "assumed.json").write_text(json.dumps({"assumed": []}))
    order = [EXTRA, *CHAIN, SIDE, *(CONCEPT_SUBS if concept else [])]
    days = [{"day": 1, "subtopics": [{"id": s} for s in order]}]
    (root / "index" / "plan.json").write_text(json.dumps({"days": days}))
    (root / "lessons" / "py").mkdir(parents=True)
    lesson = {"id": EXTRA, "status": "published", "title_vi": "x", "blocks": []}
    (root / "lessons" / "py" / f"{EXTRA}.yaml").write_text(yaml.safe_dump(lesson))
    (root / "checks").mkdir()
    for n, sid in enumerate(CHAIN):
        q = GATE_ITEM[sid]
        items = [
            {
                "id": f"R{n}",
                "type": "read_code",
                "minutes": 3,
                "difficulty": 1,
                "code": "print(1)",
                "expected_output": "1",
                "answer_md": "one",
            },
            {
                "id": q,
                "type": "write_code",
                "minutes": 6,
                "difficulty": 2,
                "prompt_md": "viet add",
                "problem_id": f"check-{q.lower()}",
            },
            {
                "id": f"X{n}",  # a level 3 item that placement must never ask
                "type": "write_code",
                "minutes": 10,
                "difficulty": 3,
                "prompt_md": "viet add 3",
                "problem_id": f"check-x{n}",
            },
        ]
        (root / "checks" / f"{sid}.yaml").write_text(
            yaml.safe_dump({"subtopic_id": sid, "items": items})
        )
        for it in (items[1], items[2]):
            pdir = root / "problems" / sid / it["problem_id"]
            (pdir / "tests").mkdir(parents=True)
            (pdir / "problem.yaml").write_text(
                yaml.safe_dump(
                    {
                        "id": it["problem_id"],
                        "subtopic_id": sid,
                        "kind": "check",
                        "title": it["problem_id"],
                        "difficulty": "easy",
                        "source": {"type": "original"},
                        "time_target_min": it["minutes"],
                        "status": "validated",
                    }
                )
            )
    if rungs:  # a placement pool for C1 and C2 (P0 mcq answer_index 1, P1 read_code "1")
        (root / "placement").mkdir()
        for spec in pl.GATES[:2]:
            items = [
                {
                    "id": spec["p0"],
                    "difficulty": 1,
                    "type": "mcq",
                    "minutes": 1,
                    "prompt_md": "pick b",
                    "choices": ["a", "b", "c"],
                    "answer_index": 1,
                    "explanation_md": "because b",
                },
                {
                    "id": spec["p1"],
                    "difficulty": 1,
                    "type": "read_code",
                    "minutes": 2,
                    "prompt_md": "what prints?",
                    "code": "print(1)",
                    "expected_output": "1",
                },
            ]
            (root / "placement" / f"{spec['subtopic_id']}.yaml").write_text(
                yaml.safe_dump({"subtopic_id": spec["subtopic_id"], "items": items})
            )
    if concept:  # hubs: C1 = level-1 mcq (answer_index 1), C2 = level-2 mcq (answer_index 2)
        (root / "placement").mkdir(exist_ok=True)
        for n, (sid, (_prereqs, c1, c2)) in enumerate(CONCEPT_SUBS.items()):
            items = []
            for level, present, ans in ((1, c1, 1), (2, c2, 2)):
                if present:
                    items.append(
                        {
                            "id": f"M{n}{level}",
                            "difficulty": level,
                            "type": "mcq",
                            "minutes": level,
                            "prompt_md": f"hub {sid} level {level}",
                            "choices": ["a", "b", "c"],
                            "answer_index": ans,
                            "explanation_md": "because",
                        }
                    )
            if items:
                (root / "placement" / f"{sid}.yaml").write_text(
                    yaml.safe_dump({"subtopic_id": sid, "items": items})
                )
    return root


@pytest.fixture
def content_dir(tmp_path: Path, request: pytest.FixtureRequest) -> Path:
    name = request.function.__name__
    return build_placement_content(
        tmp_path / "content", name.startswith("test_rung"), name.startswith("test_concept")
    )


def key(n: str) -> dict[str, str]:
    return {"Idempotency-Key": n}


def start(client, **body):
    r = client.post("/api/placement", json=body)
    assert r.status_code == 200, r.text
    return r.json()


def write_body(item: str, ok: bool = True, elapsed_ms: int = 360_000, **kw) -> dict:
    return {
        "item_id": item,
        "elapsed_ms": elapsed_ms,
        "code": "def add(a, b): return a + b",
        "verdict": "AC" if ok else "WA",
        "passed_tests": 1 if ok else 0,
        "total": 1,
        **kw,
    }


MINUTES = {"mcq": 1.0, "read_code": 2.0, "write_code": 6.0}


def drive(
    client,
    clock,
    script: dict[str, str],
    *,
    minutes=6.0,
    rungs: dict[str, str] | None = None,
    pid: int | None = None,
):
    """Play a placement to its end. script: gate code -> pass | fail | giveup for the P2 write_code
    item; rungs: "C1:P0" / "C1:P1" -> pass | fail | giveup (default pass). `pid` drives that session
    directly (deep-dives aren't surfaced by /current, which tracks only the initial sitting)."""
    rungs = rungs or {}
    if pid is not None:
        cur = client.get(f"/api/placement/{pid}").json()
    else:
        cur = client.get("/api/placement/current").json()["placement"]
    pid, active = cur["placement_id"], cur["active_ms"]
    steps = 0
    while cur["status"] == "in_progress" and cur["current"] is not None:
        c = cur["current"]
        step = c["step"]
        kind = step["type"]
        mins = minutes if kind == "write_code" else MINUTES[kind]
        clock.advance(minutes=mins)
        active += int(mins * 60_000)
        base = {"item_id": step["item_id"], "elapsed_ms": int(mins * 60_000)}
        base["session_elapsed_ms"] = active
        if kind == "write_code":
            act = script.get(c["gate"], "pass")
        else:
            act = rungs.get(f"{c['gate']}:P{c['rung']}", "pass")
        if act == "giveup":
            r = client.post(f"/api/placement/{pid}/skip", json=base)
        elif kind == "write_code":
            body = write_body(step["item_id"], act == "pass", int(mins * 60_000))
            r = client.post(f"/api/placement/{pid}/answer", json={**body, **base})
        elif kind == "mcq":
            r = client.post(
                f"/api/placement/{pid}/answer", json={**base, "choice": 1 if act == "pass" else 0}
            )
        else:
            ans = "1" if act == "pass" else "nope"
            r = client.post(f"/api/placement/{pid}/answer", json={**base, "answer": ans})
        assert r.status_code == 200, r.text
        cur = r.json()["placement"]
        steps += 1
        assert steps < 40
    return cur


def db_rows(client, model):
    with client.app.state.rt.session() as db:
        return list(db.scalars(select(model).order_by(model.id)))


def sub_row(client, sid):
    with client.app.state.rt.session() as db:
        return db.get(t.UserSubtopic, (1, sid))


def assert_parity(client):
    """score cache == scoring(events) for every subtopic, and placement never makes a 3."""
    rt = client.app.state.rt
    with rt.session() as db:
        for sid in rt.content.subtopics:
            ev = progress.load_evidence(db, rt.content, sid)
            want = sc.score(rt.content.spec_for(sid), ev).score
            assert db.get(t.UserSubtopic, (1, sid)).score == want
            assert want in (0, 1, 2), (sid, want)  # placement alone never makes 3


def set_experience(client, exp):
    r = client.put(
        "/api/profile",
        json={"target_role": "intern", "track": "swe", "language": "python", "experience": exp},
    )
    assert r.status_code == 200


def test_real_content_has_all_seven_gates():
    store = ContentStore.load(REPO_CONTENT)
    for spec in pl.GATES:
        item = pl._gate_item(store, spec["subtopic_id"], spec["p2"])
        assert item is not None, spec["code"]
        assert item["id"] == spec["p2"] and item["minutes"] == 6 and item["type"] == "write_code"
        assert spec["subtopic_id"] in store.subtopics


def test_real_pilot_rungs_resolve_and_stay_out_of_the_mastery_pool():
    store = ContentStore.load(REPO_CONTENT)
    for spec in pl.GATES:
        sid = spec["subtopic_id"]
        p0 = pl._rung_item(store, sid, spec["p0"], 0)
        p1 = pl._rung_item(store, sid, spec["p1"], 1)
        assert p0 is not None and p0["type"] == "mcq" and 0 <= p0["answer_index"] < 4
        assert p1 is not None and p1["type"] == "read_code"
        assert store.find_check_item(sid, spec["p0"]) is p0
        # the separate pool: mastery selectors and spec_for never see placement items
        assert spec["p0"] not in {i["id"] for i in store.checks[sid]}
        assert spec["p1"] not in {i["id"] for i in store.check_items(sid)[1]}


# ---- weak profile ----


def test_weak_profile_stops_at_the_first_gate_within_9_minutes(client, clock):
    set_experience(client, "none")
    v = start(client)
    assert v["experience"] == "none" and v["current"]["gate"] == "C1"
    assert v["current"]["step"]["level"] == 2 and "expected_output" not in json.dumps(v)
    end = drive(client, clock, {"C1": "fail"})
    assert end["status"] == "finished" and end["stop_reason"] == "failed_start"
    assert "Chưa cần đo thêm" in end["message_vi"]
    assert end["active_ms"] <= 9 * 60_000  # one 6 min item (placement no longer adds a level 1)
    rows = db_rows(client, t.CheckResult)
    assert [(r.level, r.passed, r.context) for r in rows] == [(2, False, "placement")]
    assert all(sub_row(client, s).score == 0 for s in CHAIN)
    assert_parity(client)
    # the 24 h lock of a real fail applies to a later mastery check
    r = client.post(f"/api/checks/{CHAIN[0]}/start")
    assert r.status_code == 409 and r.json()["error"]["code"] == "check_retry_locked"
    res = client.get(f"/api/placement/{end['placement_id']}/result").json()
    assert res["start"]["subtopic_id"] == EXTRA and res["seeded"] == []
    assert res["weak_areas"][0]["gate"] == "C1"
    # descendants of the failed gate are only labelled
    assert sub_row(client, CHAIN[1]).placement_hint == "likely_gap"
    assert sub_row(client, EXTRA).placement_hint is None


def test_none_experience_never_goes_past_c2(client, clock):
    set_experience(client, "none")
    start(client)
    end = drive(client, clock, {"C1": "pass", "C2": "pass", "C3": "pass"})
    assert end["stop_reason"] == "entry_gates_done"
    assert [g["outcome"] for g in end["gates"]][:3] == ["passed", "passed", None]
    assert end["active_ms"] == 12 * 60_000
    assert sub_row(client, CHAIN[0]).score == 2 and sub_row(client, CHAIN[2]).score == 0
    assert_parity(client)


def test_give_up_does_not_lock_and_a_p2_only_gate_has_no_known_basic(client, clock):
    set_experience(client, "none")
    start(client)
    end = drive(client, clock, {"C1": "giveup"})
    assert end["stop_reason"] == "failed_start"  # a give-up counts for stopping
    rows = db_rows(client, t.CheckResult)
    assert len(rows) == 1 and rows[0].gave_up and not rows[0].passed
    row = sub_row(client, CHAIN[0])
    assert row.known_basic is False and row.score == 0 and not row.tested_out
    assert_parity(client)
    # no lock: a mastery check can start right away
    assert client.post(f"/api/checks/{CHAIN[0]}/start").status_code == 200


# ---- strong profile ----


def test_strong_profile_seeds_only_score_2_within_the_budget(client, clock):
    set_experience(client, "some")
    start(client)
    end = drive(client, clock, dict.fromkeys(["C2", "C3", "C4", "C5", "C6", "C7"], "pass"))
    assert end["stop_reason"] == "all_gates"
    assert end["active_ms"] == 36 * 60_000 <= pl.SOFT_MS  # 6 gates x 6 min
    gate_subs = CHAIN[1:]
    for sid in gate_subs:
        r = sub_row(client, sid)
        assert r.score == 2 and r.tested_out and r.unlocked_at is not None
    assert sub_row(client, CHAIN[0]).score == 0  # C1 was never asked: label only
    assert sub_row(client, CHAIN[0]).placement_hint == "likely_known"
    assert sub_row(client, EXTRA).placement_hint == "likely_known"
    assert_parity(client)
    results = db_rows(client, t.CheckResult)
    assert {r.level for r in results} == {2} and all(r.context == "placement" for r in results)
    assert all(r.passed and r.clean for r in results)
    assert not any(r.item_id.startswith("X") for r in results)  # level 3 is never asked
    # a clean pass makes a review card in box 1
    with client.app.state.rt.session() as db:
        assert db.get(t.ReviewCard, (1, CHAIN[1])).box == 1
    res = client.get(f"/api/placement/{end['placement_id']}/result").json()
    assert res["seeded"] == sorted(gate_subs)
    assert res["counts"]["measured"] == 6 and not res["start"] and res["content_pending"]
    assert res["test_out_candidates"] == [EXTRA]


def test_clean_time_limit_is_1_5x_so_6_gates_fit_the_hard_budget(client, clock):
    set_experience(client, "some")
    start(client)
    script = dict.fromkeys(["C2", "C3", "C4", "C5", "C6", "C7"], "pass")
    end = drive(client, clock, script, minutes=9)
    assert end["active_ms"] == 54 * 60_000 <= pl.HARD_MS
    assert all(r.clean for r in db_rows(client, t.CheckResult))
    assert sub_row(client, CHAIN[6]).score == 2


def test_over_time_pass_is_not_clean_and_seeds_nothing(client, clock):
    set_experience(client, "none")
    start(client)
    end = drive(client, clock, {"C1": "pass", "C2": "pass"}, minutes=10)  # > 9 min
    assert [g["outcome"] for g in end["gates"]][:2] == ["passed_unclean", "passed_unclean"]
    assert all(sub_row(client, s).score == 0 for s in CHAIN)
    assert_parity(client)
    rows = db_rows(client, t.CheckResult)
    assert all(r.passed and not r.clean for r in rows)
    # but it is no failure: no lock
    assert client.post(f"/api/checks/{CHAIN[0]}/start").status_code == 200


# ---- stop rules ----


def test_fail_after_a_pass_stops_without_asking_further(client, clock):
    set_experience(client, "none")
    start(client)
    end = drive(client, clock, {"C1": "pass", "C2": "fail"})
    assert end["stop_reason"] == "fail_after_pass"
    assert [g["outcome"] for g in end["gates"]][:3] == ["passed", "failed", None]


def test_entry_gate_fail_probes_exactly_one_gate_below(client, clock):
    set_experience(client, "solid")  # entry C3
    v = start(client)
    assert v["current"]["gate"] == "C3" and not v["current"]["probing"]
    pid = v["placement_id"]
    clock.advance(minutes=6)
    r = client.post(
        f"/api/placement/{pid}/answer",
        json=write_body(v["current"]["step"]["item_id"], False),
    )
    nxt = r.json()["placement"]
    # no level-1 diagnostic any more: the probe of exactly one gate below (its P2) comes next
    assert nxt["current"]["gate"] == "C2" and nxt["current"]["probing"]
    assert nxt["current"]["step"]["level"] == 2
    end = drive(client, clock, {"C2": "pass"})
    gates = {g["code"]: g["outcome"] for g in end["gates"]}
    assert gates["C3"] == "failed" and gates["C2"] == "passed" and gates["C1"] is None
    assert end["stop_reason"] == "fail_after_pass"


def test_two_failed_gates_in_a_row_stop(client, clock):
    set_experience(client, "solid")
    start(client)
    end = drive(client, clock, {"C3": "fail", "C2": "giveup"})
    assert end["stop_reason"] == "two_fails"
    gates = {g["code"]: g["outcome"] for g in end["gates"]}
    assert gates["C3"] == "failed" and gates["C2"] == "gave_up" and gates["C4"] is None


def test_hard_budget_blocks_a_new_gate(client, clock):
    set_experience(client, "some")
    v = start(client)
    pid = v["placement_id"]
    clock.advance(minutes=55)
    r = client.post(
        f"/api/placement/{pid}/answer",
        json={
            **write_body(v["current"]["step"]["item_id"], True, 400_000),
            "session_elapsed_ms": 55 * 60_000,
        },
    )
    out = r.json()["placement"]
    assert out["status"] == "finished" and out["stop_reason"] == "budget"
    assert out["active_ms"] == 55 * 60_000
    assert sub_row(client, CHAIN[1]).score == 2  # what was measured stays


def test_active_time_is_monotonic_and_cannot_outrun_the_clock(client, clock):
    v = start(client)
    pid = v["placement_id"]
    clock.advance(minutes=2)
    hb = client.post(
        f"/api/placement/{pid}/heartbeat", json={"active_ms": 90_000, "item_elapsed_ms": 80_000}
    )
    assert hb.json()["active_ms"] == 90_000 and hb.json()["item_elapsed_ms"] == 80_000
    hb = client.post(f"/api/placement/{pid}/heartbeat", json={"active_ms": 30_000})
    assert hb.json()["active_ms"] == 90_000  # a stale resend never lowers it
    hb = client.post(f"/api/placement/{pid}/heartbeat", json={"active_ms": 10 * 3600_000})
    assert hb.json()["active_ms"] == 2 * 60_000 + pl.ACTIVE_SLACK_MS
    assert hb.json()["budget"]["remaining_ms"] == pl.HARD_MS - hb.json()["active_ms"]


# ---- hints are labels only ----


def test_hints_are_labels_and_real_evidence_clears_them(client, clock):
    set_experience(client, "solid")
    start(client)
    end = drive(client, clock, {"C3": "pass", "C4": "fail"})
    assert end["stop_reason"] == "fail_after_pass"
    for sid in (EXTRA, CHAIN[0], CHAIN[1]):
        r = sub_row(client, sid)
        assert r.placement_hint == "likely_known" and r.score == 0 and not r.tested_out
    assert sub_row(client, CHAIN[4]).placement_hint == "likely_gap"  # descendant of failed C4
    assert sub_row(client, CHAIN[3]).placement_hint is None  # the measured gate itself
    assert_parity(client)
    # a real pass on a labelled subtopic (test out) replaces the label
    s = client.post(f"/api/checks/{CHAIN[1]}/start", json={"context": "test_out"}).json()
    r = client.post(
        f"/api/checks/{CHAIN[1]}/answer",
        json={"session_id": s["session_id"], **write_body(s["step"]["item_id"])},
    )
    assert r.json()["score"]["after"] == 2
    assert sub_row(client, CHAIN[1]).placement_hint is None


# ---- resume / skip ----


def test_resume_mid_item_continues_at_the_same_item(client, clock):
    set_experience(client, "some")
    v = start(client)
    pid, item = v["placement_id"], v["current"]["step"]["item_id"]
    clock.advance(minutes=2)
    client.post(
        f"/api/placement/{pid}/heartbeat", json={"active_ms": 120_000, "item_elapsed_ms": 115_000}
    )
    again = start(client)  # the tab was killed and reopened
    assert again["resumed"] and again["placement_id"] == pid
    assert again["current"]["step"]["item_id"] == item and again["current"]["elapsed_ms"] == 115_000
    assert again["active_ms"] == 120_000
    assert len(db_rows(client, t.PlacementSession)) == 1
    # finish gate 1, reopen: continues at gate 2
    clock.advance(minutes=4)
    r = client.post(f"/api/placement/{pid}/answer", json=write_body(item, True, 300_000))
    assert r.status_code == 200
    again = start(client)
    assert again["resumed"] and again["current"]["gate"] == "C3"
    assert again["progress"] == {"gates_total": 6, "gates_done": 1}


def test_an_item_idle_for_24h_is_reissued_not_failed(client, clock):
    set_experience(client, "some")
    v = start(client)
    clock.advance(hours=25)
    again = start(client)
    assert again["current"]["gate"] == "C2"
    assert again["current"]["check_session_id"] != v["current"]["check_session_id"]
    assert db_rows(client, t.CheckResult) == []  # expiry writes no failure
    assert client.get(f"/api/placement/{v['placement_id']}").json()["stale"] is False
    clock.advance(days=8)
    assert client.get(f"/api/placement/{v['placement_id']}").json()["stale"] is True
    fresh = start(client, restart=True)
    assert fresh["placement_id"] != v["placement_id"] and not fresh["resumed"]
    assert db_rows(client, t.PlacementSession)[0].status == "abandoned"


def test_start_from_scratch_writes_no_check_results(client):
    set_experience(client, "none")
    v = start(client, skip=True)
    assert v["status"] == "skipped"
    assert db_rows(client, t.CheckResult) == [] and db_rows(client, t.CheckSession) == []
    assert db_rows(client, t.Attempt) == []
    assert client.get("/api/me").json()["onboarding"]["placement"] == "skipped"
    assert all(sub_row(client, s).score == 0 for s in CHAIN)
    assert client.get(f"/api/placement/{v['placement_id']}/result").status_code == 409
    assert client.get("/api/placement/current").json()["placement"]["status"] == "skipped"


def test_a8_skip_flag_without_a_session_and_onboarding_states(client, clock):
    assert client.get("/api/me").json()["onboarding"]["placement"] == "none"
    client.put("/api/profile", json={"placement": "skipped"})
    assert client.get("/api/me").json()["onboarding"]["placement"] == "skipped"
    assert client.get("/api/placement/current").json() == {"placement": None}
    set_experience(client, "none")
    start(client)  # a real placement later wins over the flag
    assert client.get("/api/me").json()["onboarding"]["placement"] == "in_progress"
    drive(client, clock, {"C1": "fail"})
    ob = client.get("/api/me").json()["onboarding"]
    assert ob == {"profile_done": True, "placement": "finished"}


def test_finish_early_keeps_results_and_drops_the_open_item(client, clock):
    set_experience(client, "some")
    v = start(client)
    pid = v["placement_id"]
    clock.advance(minutes=3)
    out = client.post(f"/api/placement/{pid}/finish", json={"active_ms": 180_000}).json()
    assert out["status"] == "finished" and out["stop_reason"] == "user_finished"
    assert db_rows(client, t.CheckResult) == []
    assert client.post(f"/api/placement/{pid}/finish").json()["status"] == "finished"
    r = client.post(f"/api/placement/{pid}/answer", json=write_body("Q023"))
    assert r.status_code == 409 and r.json()["error"]["code"] == "placement_finished"
    assert client.get(f"/api/placement/{pid}/result").json()["start"]["subtopic_id"] == EXTRA


# ---- API contract ----


def test_answer_replay_with_the_same_key_writes_once(client, clock):
    set_experience(client, "some")
    v = start(client)
    pid, item = v["placement_id"], v["current"]["step"]["item_id"]
    clock.advance(minutes=5)
    a = client.post(f"/api/placement/{pid}/answer", json=write_body(item), headers=key("k-1"))
    b = client.post(f"/api/placement/{pid}/answer", json=write_body(item), headers=key("k-1"))
    assert a.status_code == b.status_code == 200 and a.json() == b.json()
    assert b.headers.get("idempotent-replay") == "true"
    assert len(db_rows(client, t.CheckResult)) == 1
    assert len(db_rows(client, t.Attempt)) == 1


def test_errors_use_the_standard_shape(client):
    r = client.get("/api/placement/999")
    assert r.status_code == 404 and r.json()["error"]["code"] == "placement_not_found"
    v = start(client)
    r = client.post(f"/api/placement/{v['placement_id']}/answer", json=write_body("nope"))
    assert r.status_code == 409 and r.json()["error"]["code"] == "check_wrong_item"
    r = client.post(
        f"/api/placement/{v['placement_id']}/answer",
        json={"item_id": v["current"]["step"]["item_id"], "elapsed_ms": 1},
    )
    assert r.status_code == 422 and r.json()["error"]["code"] == "missing_field"
    assert db_rows(client, t.CheckResult) == []


def test_a_gate_already_at_score_2_is_skipped_and_a_locked_one_counts_as_failed(client, clock):
    set_experience(client, "none")
    # C1 tested out through a normal mastery check first
    s = client.post(f"/api/checks/{CHAIN[0]}/start", json={"context": "test_out"}).json()
    client.post(
        f"/api/checks/{CHAIN[0]}/answer",
        json={"session_id": s["session_id"], **write_body(s["step"]["item_id"])},
    )
    v = start(client)
    assert v["current"]["gate"] == "C2"  # C1 is >= 2: nothing to add
    assert v["gates"][0]["outcome"] == "known"
    client.post(f"/api/placement/{v['placement_id']}/finish")
    # C2 failed in a mastery check <24 h ago: locked, so the run stops there
    s = client.post(f"/api/checks/{CHAIN[1]}/start").json()
    client.post(
        f"/api/checks/{CHAIN[1]}/answer",
        json={"session_id": s["session_id"], **write_body(s["step"]["item_id"], False)},
    )
    v = start(client)
    assert v["status"] == "finished" and v["gates"][1]["outcome"] == "locked"
    assert v["gates"][1]["retry_after"] and v["stop_reason"] == "fail_after_pass"


# ---- rungs: P0 mcq -> P1 read_code -> P2 write_code (C1 and C2 have a placement pool) ----


def test_rung_first_item_is_an_mcq_and_never_leaks_the_answer(client):
    set_experience(client, "none")
    v = start(client)
    cur = v["current"]
    assert cur["gate"] == "C1" and cur["rung"] == 0
    step = cur["step"]
    assert step["type"] == "mcq" and step["level"] == 1 and step["minutes"] == 1
    assert step["choices"] == ["a", "b", "c"]
    blob = json.dumps(v)
    assert "answer_index" not in blob and "because b" not in blob


def test_rung_climb_p0_pass_then_p1_then_p2_then_next_gate_starts_at_p0(client, clock):
    set_experience(client, "none")
    v = start(client)
    pid = v["placement_id"]

    def play(body, mins):
        clock.advance(minutes=mins)
        r = client.post(f"/api/placement/{pid}/answer", json=body)
        assert r.status_code == 200, r.text
        return r.json()

    step = v["current"]["step"]
    out = play({"item_id": step["item_id"], "elapsed_ms": 60_000, "choice": 1}, 1)
    assert out["gate_outcome"] is None  # the gate is not decided after P0
    cur = out["placement"]["current"]
    assert cur["gate"] == "C1" and cur["rung"] == 1 and cur["step"]["type"] == "read_code"
    assert "expected_output" not in json.dumps(out)
    assert sub_row(client, CHAIN[0]).score == 1  # a clean keyed pass = tested_basic
    step = cur["step"]
    out = play({"item_id": step["item_id"], "elapsed_ms": 120_000, "answer": "1\n"}, 2)
    cur = out["placement"]["current"]
    assert cur["gate"] == "C1" and cur["rung"] == 2 and cur["step"]["level"] == 2
    assert cur["step"]["type"] == "write_code"
    out = play(write_body(cur["step"]["item_id"], True, 360_000), 6)
    assert out["gate_outcome"] == "passed" and out["score"]["after"] == 2
    cur = out["placement"]["current"]
    assert cur["gate"] == "C2" and cur["rung"] == 0 and cur["step"]["type"] == "mcq"
    results = db_rows(client, t.CheckResult)
    assert [(r.item_type, r.level, r.passed, r.clean) for r in results] == [
        ("mcq", 1, True, True),
        ("read_code", 1, True, True),
        ("write_code", 2, True, True),
    ]
    assert all(r.context == "placement" for r in results)
    assert_parity(client)


def test_rung_p0_fail_is_a_knowledge_gap_and_probes_only_the_p0_below(client, clock):
    set_experience(client, "some")  # entry C2
    v = start(client)
    assert v["current"]["gate"] == "C2" and v["current"]["step"]["type"] == "mcq"
    end = drive(client, clock, {}, rungs={"C2:P0": "fail"})
    gates = {g["code"]: g["outcome"] for g in end["gates"]}
    assert gates["C2"] == "knowledge_gap" and gates["C1"] == "known_basic"
    assert end["stop_reason"] == "fail_after_pass"
    results = db_rows(client, t.CheckResult)
    # only the two P0 items were asked: no P1 / P2 anywhere
    assert [(r.item_type, r.passed) for r in results] == [("mcq", False), ("mcq", True)]
    assert sub_row(client, CHAIN[1]).score == 0
    assert sub_row(client, CHAIN[0]).score == 1 and sub_row(client, CHAIN[0]).known_basic
    assert sub_row(client, CHAIN[2]).placement_hint == "likely_gap"
    assert_parity(client)


def test_rung_p0_fail_at_c1_stops_at_once_and_a_give_up_counts(client, clock):
    set_experience(client, "none")
    start(client)
    end = drive(client, clock, {}, rungs={"C1:P0": "giveup"})
    assert end["stop_reason"] == "failed_start"
    assert end["gates"][0]["outcome"] == "knowledge_gap"
    rows = db_rows(client, t.CheckResult)
    assert len(rows) == 1 and rows[0].gave_up and rows[0].item_type == "mcq"
    assert end["active_ms"] == 60_000 and all(sub_row(client, s).score == 0 for s in CHAIN)


def test_rung_two_p0_fails_in_a_row_stop(client, clock):
    set_experience(client, "some")
    start(client)
    end = drive(client, clock, {}, rungs={"C2:P0": "fail", "C1:P0": "fail"})
    assert end["stop_reason"] == "two_fails"
    gates = {g["code"]: g["outcome"] for g in end["gates"]}
    assert gates["C2"] == "knowledge_gap" and gates["C1"] == "knowledge_gap"


def test_rung_p1_fail_keeps_known_basic_skips_p2_and_probes_p2_below(client, clock):
    set_experience(client, "some")  # entry C2
    start(client)
    end = drive(client, clock, {"C1": "pass"}, rungs={"C2:P1": "fail"})
    gates = {g["code"]: g["outcome"] for g in end["gates"]}
    assert gates["C2"] == "failed" and gates["C1"] == "passed"
    assert end["stop_reason"] == "fail_after_pass"
    got = [(r.item_type, r.passed) for r in db_rows(client, t.CheckResult)]
    # C2: P0 pass, P1 fail (no P2); then the probe is C1's P2 only (no P0 / P1)
    assert got == [("mcq", True), ("read_code", False), ("write_code", True)]
    c2 = sub_row(client, CHAIN[1])
    assert c2.known_basic is True and c2.score == 1 and not c2.tested_out
    assert sub_row(client, CHAIN[0]).score == 2
    assert_parity(client)


def test_rung_a_gate_whose_pool_is_missing_falls_back_to_p2_only(client, clock):
    set_experience(client, "solid")  # entry C3: the synthetic content has no C3 placement pool
    v = start(client)
    assert v["current"]["gate"] == "C3" and v["current"]["rung"] == 2
    assert v["current"]["step"]["type"] == "write_code"


def test_rung_mcq_needs_a_choice_and_over_time_is_not_clean(client):
    v = start(client)
    item = v["current"]["step"]["item_id"]
    r = client.post(
        f"/api/placement/{v['placement_id']}/answer", json={"item_id": item, "elapsed_ms": 1}
    )
    assert r.status_code == 422 and r.json()["error"]["code"] == "missing_field"
    r = client.post(
        f"/api/placement/{v['placement_id']}/answer",
        json={"item_id": item, "elapsed_ms": 90_001, "choice": 1},
    )
    assert r.json()["result"]["clean"] is False  # over 1.5 x 1 min: correct but not clean
    assert sub_row(client, CHAIN[0]).score == 0  # an unclean pass is no evidence


# ---- concept phase: module self-report -> 2-rung hub gates K1.. (C1 level-1, C2 level-2 mcq) ----


def set_track(client, track):
    r = client.put(
        "/api/profile",
        json={"target_role": "intern", "track": track, "language": "python", "experience": "none"},
    )
    assert r.status_code == 200


def to_concept_offer(client, clock, track="swe"):
    """A weak profile: C1 failed -> the code ladder stops, the concept offer opens."""
    set_track(client, track)
    start(client)
    end = drive(client, clock, {"C1": "fail"})
    assert end["status"] == "in_progress" and end["phase"] == "concept_offer"
    return end


def post_modules(client, pid, modules, **kw):
    return client.post(f"/api/placement/{pid}/modules", json={"selected": modules, **kw})


def mcq(client, clock, pid, view, choice=None, *, minutes=1.0):
    """Answer the current concept mcq (choice None = "Không biết"); returns the placement view."""
    clock.advance(minutes=minutes)
    cur = view["current"]
    body = {"item_id": cur["step"]["item_id"], "elapsed_ms": int(minutes * 60_000)}
    if choice is None:
        r = client.post(f"/api/placement/{pid}/skip", json=body)
    else:
        r = client.post(f"/api/placement/{pid}/answer", json={**body, "choice": choice})
    assert r.status_code == 200, r.text
    return r.json()["placement"]


def concept_outcomes(view):
    return [g["outcome"] for g in view["gates"] if g["kind"] == "concept"]


def test_concept_offer_opens_after_the_code_ladder_and_is_track_filtered(client, clock):
    end = to_concept_offer(client, clock, "swe")
    assert end["awaiting_modules"] is True and end["current"] is None
    assert end["code_stop_reason"] == "failed_start" and end["stop_reason"] is None
    # only System Design modules whose hub has BOTH a level-1 and a level-2 mcq
    assert [o["module"] for o in end["concept_offer"]] == ["sd.data", "sd.caching"]
    assert [o["hub_subtopic_id"] for o in end["concept_offer"]] == [HUB_DATA, HUB_CACHE]
    assert "ml.rag_agents" not in json.dumps(end["concept_offer"])
    assert "answer_index" not in json.dumps(end)
    pid = end["placement_id"]
    # the sitting is waiting: no item can be answered, a resume shows the same offer
    r = client.post(f"/api/placement/{pid}/answer", json={"item_id": "x", "elapsed_ms": 1})
    assert r.status_code == 409 and r.json()["error"]["code"] == "placement_awaiting_modules"
    again = start(client)
    assert again["resumed"] and again["phase"] == "concept_offer"
    assert again["concept_offer"] == end["concept_offer"]
    assert client.get("/api/me").json()["onboarding"]["placement"] == "in_progress"


def test_concept_offer_for_the_ai_track_only_lists_ai_modules(client, clock):
    end = to_concept_offer(client, clock, "ai")
    assert [o["module"] for o in end["concept_offer"]] == ["ml.rag_agents"]


def test_concept_hub_without_a_level_2_mcq_or_without_items_is_not_offered(client, clock):
    end = to_concept_offer(client, clock)
    mods = {o["module"] for o in end["concept_offer"]}
    assert "sd.api" not in mods  # hub has only a level-1 mcq
    assert "sd.networking" not in mods  # nothing authored
    pid = end["placement_id"]
    assert post_modules(client, pid, ["bogus"]).status_code == 422
    # selecting an unauthored (but real) module is ignored: nothing to run -> the sitting ends
    out = post_modules(client, pid, ["sd.api", "sd.networking"]).json()
    assert out["status"] == "finished" and out["stop_reason"] == "failed_start"
    assert not [g for g in out["gates"] if g["kind"] == "concept"]


def test_concept_select_starts_the_first_hub_at_its_c1_mcq(client, clock):
    end = to_concept_offer(client, clock)
    pid = end["placement_id"]
    v = post_modules(client, pid, ["sd.caching", "sd.data"]).json()  # tree order wins
    assert v["phase"] == "concept" and v["awaiting_modules"] is False
    cur = v["current"]
    assert cur["kind"] == "concept" and cur["gate"] == "K1" and cur["module"] == "sd.data"
    assert cur["subtopic_id"] == HUB_DATA and cur["rung"] == 0 and not cur["probing"]
    assert cur["step"]["type"] == "mcq" and cur["step"]["level"] == 1
    assert cur["step"]["choices"] == ["a", "b", "c"]
    assert [g["code"] for g in v["gates"] if g["kind"] == "concept"] == ["K1", "K2"]
    assert "answer_index" not in json.dumps(v) and "because" not in json.dumps(v)
    # a second selection is refused
    r = post_modules(client, pid, ["sd.data"])
    assert r.status_code == 409 and r.json()["error"]["code"] == "placement_not_awaiting_modules"


def test_concept_c1_pass_serves_c2_and_a_c2_pass_scores_2_then_the_next_hub(client, clock):
    end = to_concept_offer(client, clock)
    pid = end["placement_id"]
    v = post_modules(client, pid, ["sd.data", "sd.caching"]).json()
    v = mcq(client, clock, pid, v, 1)  # C1 pass
    cur = v["current"]
    assert cur["gate"] == "K1" and cur["rung"] == 2 and cur["step"]["level"] == 2
    assert cur["step"]["type"] == "mcq" and cur["step"]["minutes"] == 2
    row = sub_row(client, HUB_DATA)
    assert row.score == 1 and not row.tested_out  # one keyed pass = tested_basic only
    v = mcq(client, clock, pid, v, 2, minutes=2.0)  # C2 pass (keyed, level 2)
    row = sub_row(client, HUB_DATA)
    assert row.score == 2 and row.tested_out and row.unlocked_at is not None
    assert row.known_basic is False and row.placement_hint is None
    cur = v["current"]
    assert cur["gate"] == "K2" and cur["subtopic_id"] == HUB_CACHE and cur["rung"] == 0
    assert concept_outcomes(v) == ["passed", None]
    # display-only inference: the hub's prerequisite is labelled, never scored
    intro = sub_row(client, "sd.data.intro")
    assert intro.placement_hint == "likely_known" and intro.score == 0
    v = mcq(client, clock, pid, v, 1)
    v = mcq(client, clock, pid, v, 2, minutes=2.0)
    assert v["status"] == "finished" and v["stop_reason"] == "concept_done"
    assert "module khái niệm" in v["message_vi"] and v["current"] is None
    assert sub_row(client, HUB_CACHE).score == 2
    results = [
        (r.subtopic_id, r.item_type, r.level, r.passed, r.context)
        for r in db_rows(client, t.CheckResult)
        if r.subtopic_id in (HUB_DATA, HUB_CACHE)
    ]
    assert results == [
        (HUB_DATA, "mcq", 1, True, "placement"),
        (HUB_DATA, "mcq", 2, True, "placement"),
        (HUB_CACHE, "mcq", 1, True, "placement"),
        (HUB_CACHE, "mcq", 2, True, "placement"),
    ]
    assert_parity(client)
    res = client.get(f"/api/placement/{pid}/result").json()
    assert [c["outcome"] for c in res["concept"]] == ["passed", "passed"]
    assert [c["score"] for c in res["concept"]] == [2, 2]
    assert set(res["seeded"]) >= {HUB_DATA, HUB_CACHE}


def test_concept_c1_fail_or_skip_skips_c2_labels_gap_and_moves_on(client, clock):
    end = to_concept_offer(client, clock)
    pid = end["placement_id"]
    v = post_modules(client, pid, ["sd.data", "sd.caching"]).json()
    v = mcq(client, clock, pid, v, 0)  # C1 wrong
    cur = v["current"]
    assert cur["gate"] == "K2" and cur["rung"] == 0 and cur["subtopic_id"] == HUB_CACHE
    assert concept_outcomes(v) == ["knowledge_gap", None]
    assert sub_row(client, HUB_DATA).score == 0 and sub_row(client, HUB_DATA).known_basic is False
    # descendants of the failed hub are only labelled
    assert sub_row(client, "sd.caching.eviction_invalidation").placement_hint == "likely_gap"
    v = mcq(client, clock, pid, v, None)  # "Không biết" on K2's C1
    assert v["status"] == "finished" and v["stop_reason"] == "concept_done"
    got = [
        (r.subtopic_id, r.level, r.passed, r.gave_up)
        for r in db_rows(client, t.CheckResult)
        if r.item_type == "mcq"
    ]
    assert got == [(HUB_DATA, 1, False, False), (HUB_CACHE, 1, False, True)]  # never a C2
    assert all(sub_row(client, s).score == 0 for s in (HUB_DATA, HUB_CACHE))
    assert_parity(client)


def test_concept_c2_fail_keeps_the_c1_basic_pass_only(client, clock):
    end = to_concept_offer(client, clock)
    pid = end["placement_id"]
    v = post_modules(client, pid, ["sd.data"]).json()
    v = mcq(client, clock, pid, v, 1)
    v = mcq(client, clock, pid, v, 0, minutes=2.0)  # C2 wrong
    assert v["status"] == "finished" and v["stop_reason"] == "concept_done"
    assert concept_outcomes(v) == ["failed"]
    row = sub_row(client, HUB_DATA)
    assert row.score == 1 and row.known_basic is True and not row.tested_out
    assert sub_row(client, "sd.data.intro").placement_hint is None  # a C2 fail labels nothing
    assert_parity(client)


def test_concept_over_time_c2_pass_is_not_clean_and_scores_nothing_more(client, clock):
    end = to_concept_offer(client, clock)
    pid = end["placement_id"]
    v = post_modules(client, pid, ["sd.data"]).json()
    v = mcq(client, clock, pid, v, 1)
    v = mcq(client, clock, pid, v, 2, minutes=4.0)  # > 1.5 x 2 min
    assert concept_outcomes(v) == ["passed_unclean"]
    row = sub_row(client, HUB_DATA)
    assert row.score == 1 and not row.tested_out  # only the C1 keyed pass counts


def test_concept_empty_selection_ends_with_the_code_stop_reason(client, clock):
    end = to_concept_offer(client, clock)
    out = post_modules(client, end["placement_id"], []).json()
    assert out["status"] == "finished" and out["stop_reason"] == "failed_start"
    assert out["phase"] == "finished" and out["concept_offer"] is None
    assert "Chưa cần đo thêm" in out["message_vi"]
    assert not [g for g in out["gates"] if g["kind"] == "concept"]
    assert pl.MESSAGES["concept_skipped"] and pl.MESSAGES["concept_done"]


def test_concept_finish_early_during_the_offer_keeps_the_code_results(client, clock):
    end = to_concept_offer(client, clock)
    out = client.post(f"/api/placement/{end['placement_id']}/finish").json()
    assert out["status"] == "finished" and out["stop_reason"] == "user_finished"


def test_concept_budget_guard_stops_when_no_c1_fits(client, clock):
    end = to_concept_offer(client, clock)
    pid = end["placement_id"]
    clock.advance(minutes=60)
    v = post_modules(client, pid, ["sd.data"], active_ms=int(59.5 * 60_000)).json()
    assert v["status"] == "finished" and v["stop_reason"] == "budget"  # 59.5 + 1 > 60
    assert db_rows(client, t.CheckResult)[-1].level == 2  # nothing was asked in the concept phase


# ---- deep-dive (module-scoped, knowledge rungs only) ----


def test_rung_deep_dive_builds_gates_for_probed_subtopics_only(client, clock):
    v = start(client, kind="deep_dive", module="py.core")
    assert v["kind"] == "deep_dive" and v["scope"] == "py.core" and v["phase"] == "deep"
    assert [g["subtopic_id"] for g in v["gates"]] == ["py.core.strings"]
    assert v["gates"][0]["kind"] == "deep" and v["gates"][0]["code"] == "D1"
    cur = v["current"]
    assert cur["kind"] == "deep" and cur["rung"] == 0 and cur["step"]["type"] == "mcq"
    with client.app.state.rt.session() as db:
        ps = db.get(t.PlacementSession, v["placement_id"])
        assert ps.state["gates"][0]["rung_items"][2] is None


def test_rung_deep_dive_clean_passes_score_1_never_2_or_unlock(client, clock):
    v = start(client, kind="deep_dive", module="py.core")
    end = drive(client, clock, {}, pid=v["placement_id"])
    assert end["status"] == "finished" and end["stop_reason"] == "deep_dive_done"
    assert end["message_vi"] == pl.MESSAGES["deep_dive_done"]
    assert end["gates"][0]["rung_results"] == {"0": "passed", "1": "passed"}
    assert end["gates"][0]["outcome"] == "known_basic"
    row = sub_row(client, "py.core.strings")
    assert row.score == 1 and row.unlocked_at is None and row.known_basic
    rows = db_rows(client, t.CheckResult)
    assert {(r.level, r.context) for r in rows} == {(1, "placement")}
    assert v["placement_id"] == end["placement_id"]
    assert_parity(client)


def test_rung_deep_dive_p0_fail_is_a_gap_and_skips_p1(client, clock):
    v = start(client, kind="deep_dive", module="py.core")
    end = drive(client, clock, {}, rungs={"D1:P0": "fail"}, pid=v["placement_id"])
    assert end["stop_reason"] == "deep_dive_done"
    assert end["gates"][0]["outcome"] == "knowledge_gap"
    assert end["gates"][0]["rung_results"] == {"0": "failed"}
    assert sub_row(client, "py.core.strings").score == 0


def test_rung_deep_dive_module_without_probes_stops_at_once(client, clock):
    v = start(client, kind="deep_dive", module="dsa.arrays_strings")
    assert v["status"] == "finished" and v["stop_reason"] == "deep_dive_done"
    assert v["gates"] == [] and v["current"] is None


def test_rung_deep_dive_validates_module(client, clock):
    r = client.post("/api/placement", json={"kind": "deep_dive"})
    assert r.status_code == 422
    r = client.post("/api/placement", json={"kind": "deep_dive", "module": "nope.nope"})
    assert r.status_code == 422


def test_rung_deep_dive_coexists_with_the_initial_sitting(client, clock):
    first = start(client)
    deep = start(client, kind="deep_dive", module="py.core")
    assert deep["placement_id"] != first["placement_id"] and not deep["resumed"]
    # The initial sitting is left untouched (not abandoned); it stays what current/onboarding see.
    old = client.get(f"/api/placement/{first['placement_id']}").json()
    assert old["status"] == "in_progress"
    assert (
        client.get("/api/placement/current").json()["placement"]["placement_id"]
        == first["placement_id"]
    )
    assert client.get("/api/me").json()["onboarding"]["placement"] == "in_progress"


def test_rung_deep_dive_p0_pass_p1_fail_still_score_1_no_unlock(client, clock):
    v = start(client, kind="deep_dive", module="py.core")
    end = drive(client, clock, {}, rungs={"D1:P1": "fail"}, pid=v["placement_id"])
    assert end["stop_reason"] == "deep_dive_done"
    assert end["gates"][0]["rung_results"] == {"0": "passed", "1": "failed"}
    row = sub_row(client, "py.core.strings")
    assert row.score == 1 and row.unlocked_at is None and row.known_basic
    assert {(r.level, r.context) for r in db_rows(client, t.CheckResult)} == {(1, "placement")}


def test_rung_deep_dive_skips_already_mastered_subtopics(client, clock):
    with client.app.state.rt.session() as db:
        row = db.get(t.UserSubtopic, (1, "py.core.strings"))
        row.score = 2
        db.commit()
    v = start(client, kind="deep_dive", module="py.core")
    # py.core.strings is the only probed subtopic today; mastered -> no gates -> stops at once.
    assert v["gates"] == [] and v["status"] == "finished" and v["stop_reason"] == "deep_dive_done"
