"""Placement Phase A (A10): gate ladder, stop rules, budget, seeding only score 2 (SPEC 5.6)."""

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
CHAIN = [g[1] for g in pl.GATES]
GATE_ITEM = {g[1]: g[2] for g in pl.GATES}
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


def build_placement_content(root: Path) -> Path:
    (root / "index").mkdir(parents=True)
    subs = [_sub(EXTRA, 1, [])]
    prev = EXTRA
    for i, sid in enumerate(CHAIN):
        subs.append(_sub(sid, i + 2, [prev]))
        prev = sid
    subs.append(_sub(SIDE, 20, [CHAIN[0]]))
    (root / "index" / "subtopics.json").write_text(json.dumps({"subtopics": subs}))
    (root / "index" / "assumed.json").write_text(json.dumps({"assumed": []}))
    order = [EXTRA, *CHAIN, SIDE]
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
    return root


@pytest.fixture
def content_dir(tmp_path: Path) -> Path:
    return build_placement_content(tmp_path / "content")


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


def drive(client, clock, script: dict[str, str], *, l1="fail", minutes=6.0, l1_minutes=3.0):
    """Play the current placement to its end. script: gate code -> pass | fail | giveup."""
    cur = client.get("/api/placement/current").json()["placement"]
    pid, active = cur["placement_id"], cur["active_ms"]
    steps = 0
    while cur["status"] == "in_progress":
        c = cur["current"]
        step = c["step"]
        mins = minutes if step["level"] == 2 else l1_minutes
        clock.advance(minutes=mins)
        active += int(mins * 60_000)
        base = {"item_id": step["item_id"], "elapsed_ms": int(mins * 60_000)}
        base["session_elapsed_ms"] = active
        if step["level"] == 2:
            act = script[c["gate"]]
            if act == "giveup":
                r = client.post(f"/api/placement/{pid}/skip", json=base)
            else:
                body = write_body(step["item_id"], act == "pass", int(mins * 60_000))
                r = client.post(f"/api/placement/{pid}/answer", json={**body, **base})
        else:
            ans = "1" if l1 == "pass" else "nope"
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
    """score cache == scoring(events) for every subtopic, and nothing placement-made is 1 or 3."""
    rt = client.app.state.rt
    with rt.session() as db:
        for sid in rt.content.subtopics:
            ev = progress.load_evidence(db, rt.content, sid)
            want = sc.score(rt.content.spec_for(sid), ev).score
            assert db.get(t.UserSubtopic, (1, sid)).score == want
            assert want in (0, 2), (sid, want)  # placement alone never makes 1 or 3


def set_experience(client, exp):
    r = client.put(
        "/api/profile",
        json={"target_role": "intern", "track": "swe", "language": "python", "experience": exp},
    )
    assert r.status_code == 200


def test_real_content_has_all_seven_gates():
    store = ContentStore.load(REPO_CONTENT)
    for code, sid, item_id, _ in pl.GATES:
        item = pl._gate_item(store, sid, item_id)
        assert item is not None, code
        assert item["id"] == item_id and item["minutes"] == 6 and item["type"] == "write_code"
        assert sid in store.subtopics


# ---- weak profile ----


def test_weak_profile_stops_at_the_first_gate_within_9_minutes(client, clock):
    set_experience(client, "none")
    v = start(client)
    assert v["experience"] == "none" and v["current"]["gate"] == "C1"
    assert v["current"]["step"]["level"] == 2 and "expected_output" not in json.dumps(v)
    end = drive(client, clock, {"C1": "fail"}, l1="fail")
    assert end["status"] == "finished" and end["stop_reason"] == "failed_start"
    assert "Chưa cần đo thêm" in end["message_vi"]
    assert end["active_ms"] <= 9 * 60_000  # 6 min item + 3 min level 1 (UI_SPEC 2.7)
    rows = db_rows(client, t.CheckResult)
    assert [(r.level, r.passed, r.context) for r in rows] == [
        (2, False, "placement"),
        (1, False, "placement"),
    ]
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


def test_give_up_does_not_lock_and_level1_pass_sets_known_basic_only(client, clock):
    set_experience(client, "none")
    start(client)
    end = drive(client, clock, {"C1": "giveup"}, l1="pass")
    assert end["stop_reason"] == "failed_start"  # a give-up counts for stopping
    rows = db_rows(client, t.CheckResult)
    assert rows[0].gave_up and not rows[0].passed
    assert rows[1].level == 1 and rows[1].passed
    row = sub_row(client, CHAIN[0])
    assert row.known_basic is True and row.score == 0 and not row.tested_out
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
    end = drive(client, clock, {"C1": "pass", "C2": "fail"}, l1="fail")
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
    assert nxt["current"]["step"]["level"] == 1  # diagnostic of the failed gate first
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
    end = drive(client, clock, {"C3": "pass", "C4": "fail"}, l1="fail")
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
