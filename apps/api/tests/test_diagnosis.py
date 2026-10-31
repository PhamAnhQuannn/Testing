"""Skill diagnosis (SPEC 5.7): pure unit tests plus GET /api/diagnosis."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml

from app.models import tables as t
from app.services.concepts import registry_of, slugify
from app.services.content_loader import TRACKS, module_name, track_of
from app.services.diagnosis import (
    ConceptResult,
    SubtopicView,
    concept_status,
    diagnose,
    level_of,
    pick_concepts,
    readiness_summary,
)


def v(i, score=0, measured=None, hint=None, module="py.a", section="py", concepts=()):
    if measured is None:
        measured = score > 0
    return SubtopicView(i, section, module, f"N {i}", score, measured, hint, True, list(concepts))


def mod(views, **kw):
    return diagnose(views, **kw)[0].modules[0]


@pytest.mark.parametrize(
    "mean,level",
    [(0.0, "Mới"), (0.74, "Mới"), (0.75, "Cơ bản"), (1.49, "Cơ bản"), (1.5, "Vững"),
     (2.24, "Vững"), (2.25, "Thành thạo"), (3.0, "Thành thạo")],
)  # fmt: skip
def test_level_bands(mean, level) -> None:
    assert level_of(mean, 1.0) == level


def test_low_coverage_is_insufficient() -> None:
    views = [v("a", 3)] + [v(f"x{i}") for i in range(4)]  # coverage 0.2
    m = mod(views)
    assert m.level == "Chưa đủ dữ liệu" and m.tier == "suy luận"  # 1 measured but < 0.4


def test_effective_scores() -> None:
    m = mod([v("a", 2), v("b", hint="likely_known"), v("c", hint="likely_gap"), v("d")])
    assert m.mean == round((2 + 2.0 + 0.5) / 3, 2)  # d excluded
    assert m.not_assessed_count == 1
    assert m.coverage == 0.25


def test_tier_rules() -> None:
    # "đã đo" requires coverage >= 0.4 (same bar as the level band)
    assert mod([v("a", 1), v("b", 1), v("c")]).tier == "đã đo"  # coverage 0.67
    assert mod([v("a", 1), v("b", 1)] + [v(f"x{i}") for i in range(4)]).tier == "suy luận"
    assert mod([v("a", 1)] + [v(f"x{i}") for i in range(5)]).tier == "suy luận"  # 1 measured, <0.4
    assert mod([v("a", 1)] + [v(f"x{i}", hint="likely_gap") for i in range(5)]).tier == "suy luận"
    assert mod([v("a", hint="likely_known")]).tier == "suy luận"
    assert mod([v("a")]).tier == "chưa đo"
    assert mod([v(f"x{i}") for i in range(3)]).tier == "chưa đo"  # nothing measured or hinted


def test_strong_excludes_hints_and_caps() -> None:
    views = [v(f"s{i}", 2 + i % 2) for i in range(7)] + [v("h", hint="likely_known")]
    strong = mod(views).strong
    assert len(strong) == 5 and all(s["score"] >= 2 for s in strong)
    assert [s["score"] for s in strong] == sorted((s["score"] for s in strong), reverse=True)
    assert "h" not in {s["subtopic_id"] for s in strong}


def test_improve_ranking_and_caps() -> None:
    views = [
        v("firm0", 0, measured=True),
        v("firm1", 1),
        v("gap", hint="likely_gap"),
        v("block", 1),
        v("ok", 2),
        v("none"),
    ]
    imp = mod(views, blocking_ids=frozenset({"block"})).improve
    assert [i["subtopic_id"] for i in imp] == ["block", "firm0", "firm1", "gap"]
    assert [i["firm"] for i in imp] == [True, True, True, False]
    assert imp[-1]["state"] == "likely_gap" and imp[0]["state"] == "measured"
    many = [v(f"m{i}", 1, concepts="abcde") for i in range(9)]
    top = mod(many).improve
    assert len(top) == 5 and top[0]["concepts"] == ["a", "b", "c"] and top[0]["has_lesson"]


def test_domain_aggregates_modules_and_order() -> None:
    views = [
        v("ml1", 2, module="ml.llm", section="ml"),
        v("sd1", 1, module="sd.api", section="sd"),
        v("py1", 3, module="py.b"),
        v("py2", 1, module="py.a"),
        v("cs1", 1, module="cs.complexity", section="cs"),
    ]
    doms = diagnose(views)
    assert [d.section for d in doms] == ["py", "cs", "sd", "ml"]
    py = doms[0]
    assert py.track == "foundation" and [m.module for m in py.modules] == ["py.b", "py.a"]
    assert py.mean == 2.0 and py.coverage == 1.0 and py.level == "Vững"


def test_pick_concepts() -> None:
    node = {
        "concepts_vi": [
            {"text": "adv", "level": "nang_cao"},
            {"text": "b1", "level": "co_ban"},
            {"text": "b2", "level": "co_ban"},
            {"text": "b3", "level": "co_ban"},
        ],
        "key_concepts": ["k"],
    }
    assert pick_concepts(node) == ["b1", "b2", "b3"]
    assert pick_concepts({"key_concepts": list("wxyz")}) == ["w", "x", "y"]
    assert pick_concepts({}) == []


def test_module_name_fallback() -> None:
    assert module_name("dsa.trees") == "Cây"
    assert module_name("zz.some_new_mod") == "Some new mod"


def test_every_index_section_in_exactly_one_track() -> None:
    idx = Path(__file__).resolve().parents[3] / "content" / "index" / "subtopics.json"
    sections = {s["section"] for s in json.loads(idx.read_text(encoding="utf-8"))["subtopics"]}
    for sec in sections:
        assert sum(sec in tr["sections"] for tr in TRACKS) == 1, sec
        assert track_of(sec) != "other"


def test_api_shape_and_hint_not_strong(client) -> None:
    with client.app.state.rt.session() as db:
        for sid, hint in (("py.a.two", "likely_known"), ("py.a.three", "likely_gap")):
            row = db.get(t.UserSubtopic, (1, sid))
            row.placement_hint = hint
        db.commit()
    r = client.get("/api/diagnosis")
    assert r.status_code == 200
    body = r.json()
    assert [tr["key"] for tr in body["tracks"]] == ["foundation", "system_design", "ai"]
    (dom,) = body["domains"]
    assert dom["section"] == "py" and dom["track"] == "foundation"
    assert {"level", "mean", "coverage", "tier", "name_vi"} <= dom.keys()
    (m,) = dom["modules"]
    assert set(m) >= {"module", "name_vi", "level", "mean", "coverage", "tier", "strong",
                      "improve", "not_assessed_count"}  # fmt: skip
    assert m["strong"] == []
    assert m["tier"] != "đã đo" and m["tier"] == "suy luận"
    ids = [i["subtopic_id"] for i in m["improve"]]
    assert ids == ["py.a.three"]
    assert m["improve"][0]["state"] == "likely_gap" and m["improve"][0]["firm"] is False
    assert m["not_assessed_count"] == 1


def rv(i, target, score=0, measured=None, hint=None):
    if measured is None:
        measured = score > 0
    return SubtopicView(i, "py", "py.a", f"N {i}", score, measured, hint, True, [], target, False)


def test_role_stats_count_only_real_evidence() -> None:
    views = [rv("a", 3, 1), rv("b", 2, hint="likely_known"), rv("c", 0, 3), rv("d", 2, 3)]
    m = mod(views)
    assert m.role_relevant == 3  # "c" has no target
    assert m.gap == 2 + 2 + 0  # a: 3-1, b: inferred does not count, d: met
    assert m.readiness == round((1 + 0 + 2) / 7, 2)
    assert m.unmeasured_relevant == 1
    # real-evidence-only: a (1<3) and b (unmeasured) are below; d (met) is not
    assert m.below_target == 2


def test_improve_prioritises_largest_gap() -> None:
    m = mod([rv("small", 2, 1), rv("big", 3, 0, measured=True), rv("mid", 3, 1)])
    assert [i["subtopic_id"] for i in m.improve][0] == "big"
    assert m.improve[0]["gap"] == 3


def test_readiness_summary_and_warning() -> None:
    views = [rv("a", 2, 2), rv("b", 2), rv("c", 2)]
    doms = diagnose(views)
    s = readiness_summary(doms, views)
    assert s["readiness_pct"] == 33 and s["coverage_warning"] is True
    assert "Phần lớn" in s["coverage_message"]
    ok = [rv("a", 2, 2), rv("b", 2, 2)]
    assert readiness_summary(diagnose(ok), ok)["coverage_warning"] is False
    assert readiness_summary([], [])["readiness_pct"] is None  # no role targets -> no false 0%


ROLES8 = [(tr, lv) for tr in ("swe", "ai") for lv in ("intern", "fresher", "junior", "senior")]


@pytest.mark.parametrize("track,level", ROLES8)
def test_api_role_combos(client, track, level) -> None:
    r = client.get(f"/api/diagnosis?role={track}-{level}")
    assert r.status_code == 200
    body = r.json()
    label = ("SWE" if track == "swe" else "AI Engineer") + " " + level.capitalize()
    assert body["role"] == {
        "track": track, "level": level, "key": f"{track}-{level}", "label_vi": label,
    }  # fmt: skip
    assert [lv["level"] for lv in body["levels"]] == ["intern", "fresher", "junior", "senior"]
    assert all({"readiness_pct", "label_vi"} <= lv.keys() for lv in body["levels"])


def test_api_legacy_new_grad_maps_to_fresher(client) -> None:
    body = client.get("/api/diagnosis?role=ai-new_grad").json()
    assert body["role"]["level"] == "fresher" and body["role"]["key"] == "ai-fresher"


def test_api_default_role_from_settings(client) -> None:
    client.put("/api/profile", json={"target_role": "junior", "track": "ai"})
    assert client.get("/api/diagnosis").json()["role"]["key"] == "ai-junior"


def test_gap_non_decreasing_across_levels() -> None:
    # Per-subtopic targets are monotonic intern <= fresher <= junior <= senior, so the total gap is
    # non-decreasing as the level rises. (readiness % is per-level and NOT necessarily monotonic: a
    # subtopic whose target grows 0->n enters the relevant set and can shift the ratio either way.)
    targets = {"a": (1, 2, 3, 3), "b": (1, 1, 2, 3), "c": (2, 2, 3, 3)}
    scores = {"a": 1, "b": 2, "c": 0}
    gaps = []
    for idx in range(4):
        views = [rv(i, targets[i][idx], scores[i]) for i in targets]
        gaps.append(sum(d.gap for d in diagnose(views)))
    assert gaps == sorted(gaps) and gaps[0] < gaps[-1]


def test_api_role_param(client) -> None:
    body = client.get("/api/diagnosis?role=ai-fresher").json()
    assert body["role"]["key"] == "ai-fresher" and body["role"]["label_vi"]
    assert {"readiness_pct", "coverage_warning"} <= body.keys()
    assert client.get("/api/diagnosis?role=nope").status_code == 400
    assert client.get("/api/diagnosis").json()["role"]["key"] == "swe-intern"


def cr(slug, item, passed, text=None):
    return ConceptResult(slug, text or slug.title(), item, passed, "mcq")


def test_concept_status_thresholds() -> None:
    out = concept_status(
        [
            cr("a", "Q1", False), cr("a", "Q2", False),  # two independent misses -> weak
            cr("b", "Q3", False),  # one lone miss -> suspected, never weak
            cr("c", "Q4", True),  # hit only -> ok (omitted)
        ]
    )  # fmt: skip
    assert out == [
        {"slug": "a", "text": "A", "status": "weak", "n_hit": 0, "n_miss": 2},
        {"slug": "b", "text": "B", "status": "suspected", "n_hit": 0, "n_miss": 1},
    ]
    assert concept_status([]) == []


def test_concept_status_hit_wins_and_dedupes() -> None:
    out = concept_status(
        [cr("a", "Q1", False), cr("a", "Q1", True), cr("a", "Q2", False), cr("a", "Q2", False)]
    )
    assert out == [{"slug": "a", "text": "A", "status": "suspected", "n_hit": 1, "n_miss": 1}]


def test_concept_status_orders_weak_first() -> None:
    out = concept_status([cr("a", "Q1", False), cr("z", "Q2", False), cr("z", "Q3", False)])
    assert [c["slug"] for c in out] == ["z", "a"]


def test_slugify_and_registry() -> None:
    assert slugify("Vòng lặp for (cơ bản)!") == "vong-lap-for"
    assert slugify("  List  comprehension ") == "list-comprehension"
    assert len(slugify("x" * 100)) == 40
    node = {"concepts_vi": [{"text": "Biến (var)", "level": "basic"}], "key_concepts": ["zzz"]}
    assert registry_of(node) == {"bien": "Biến (var)"}
    assert registry_of({"key_concepts": ["Two Pointers"]}) == {"two-pointers": "Two Pointers"}


def test_registry_problems_flags_collisions_and_empty() -> None:
    from app.services.concepts import registry_problems

    assert registry_problems({"key_concepts": ["C", "C++"]})  # both slugify to "c"
    assert registry_problems({"key_concepts": ["!!!"]})  # empty slug
    assert registry_problems({"key_concepts": ["heap", "binary search"]}) == []


def test_api_concept_status_empty_without_tags(client) -> None:
    with client.app.state.rt.session() as db:
        db.get(t.UserSubtopic, (1, "py.a.two")).placement_hint = "likely_gap"
        db.commit()
    (m,) = client.get("/api/diagnosis").json()["domains"][0]["modules"]
    assert m["improve"] and all(i["concept_status"] == [] for i in m["improve"])


def test_api_concept_status_from_tagged_items(content_dir, make_client) -> None:
    idx = content_dir / "index" / "subtopics.json"
    subs = json.loads(idx.read_text())
    sub = next(x for x in subs["subtopics"] if x["id"] == "py.a.one")
    sub["concepts_vi"] = [{"text": "Vòng lặp", "level": "basic"}]
    idx.write_text(json.dumps(subs))
    cpath = content_dir / "checks" / "py.a.one.yaml"
    data = yaml.safe_load(cpath.read_text())
    for item in data["items"]:
        if item["id"] in ("Q1", "Q2"):
            item["concepts"] = ["vong-lap", "bogus"]  # unknown slug is ignored
    cpath.write_text(yaml.safe_dump(data))
    client = make_client()
    assert client.app.state.rt.content.item_concepts("py.a.one", "Q1") == ["vong-lap"]
    with client.app.state.rt.session() as db:
        for item_id in ("Q1", "Q2"):
            db.add(
                t.CheckResult(
                    user_id=1, subtopic_id="py.a.one", item_id=item_id, level=1, passed=False,
                    taken_at=datetime(2026, 1, 1, tzinfo=UTC), item_type="mcq",
                )
            )  # fmt: skip
        db.get(t.UserSubtopic, (1, "py.a.one")).score = 1
        db.commit()
    body = client.get("/api/diagnosis").json()
    improve = [i for d in body["domains"] for m in d["modules"] for i in m["improve"]]
    one = next(i for i in improve if i["subtopic_id"] == "py.a.one")
    assert one["concept_status"] == [
        {"slug": "vong-lap", "text": "Vòng lặp", "status": "weak", "n_hit": 0, "n_miss": 2}
    ]
