"""Snapshot the parts of skill_tree.json and plan.json the app needs into content/index/.

    uv run python tools/sync_tree.py <skill_tree.json> <plan.json> [--out content/index]

Two selection rules feed the snapshot:
  1. The 40 MVP subtopics (SPEC 4.1): ids of plan days 1-12 in plan order, `bh.*` excluded, each
     counted once. These are the py/dsa/cs foundations.
  2. Two extra tracks selected whole by section/module, because they are NOT in the plan days:
     System Design (section `sd`, 86) and the AI-engineer LLM subset of `ml`
     (`ml.llm`, `ml.rag_agents`, `ml.llm_eval_serving`, `ml.system_design`, 39). They are appended
     after the 40 in tree order. These are concept tracks (SPEC 5.2); their prerequisites that fall
     outside the shipped set go to assumed.json (no plan `assumed_known` membership is required for
     this curated selection).

Every output file records the sha256 of its source files, so the committed snapshot shows which
version of the sources it was built from (CI cannot read them).
"""

import argparse
from pathlib import Path

from common import CONTENT, dump_json, load_json, sha256_file

MVP_LAST_DAY = 12
PLAN_SNAPSHOT_LAST_DAY = 14

# Extra tracks selected whole (not in the plan days).
EXTRA_SECTIONS = {"sd"}
EXTRA_MODULES = {"ml.llm", "ml.rag_agents", "ml.llm_eval_serving", "ml.system_design"}

# Expected shipped counts, asserted so an upstream tree edit can't silently change the snapshot.
PLAN_MVP_COUNT = 40
EXPECTED_SD = 86
EXPECTED_ML4 = 39
EXPECTED_TOTAL = PLAN_MVP_COUNT + EXPECTED_SD + EXPECTED_ML4  # 165

# Node fields the app uses (SPEC 4.2); optional ones are skipped when a node lacks them.
NODE_FIELDS = [
    "name_vi", "order", "summary_vi", "mastery_bar_vi", "prerequisites", "lang_prereqs",
    "key_concepts", "concepts_vi", "examples_vi", "beginner_note_vi", "starter_code_vi",
    "example_problems", "bank_topics", "bank_counts", "target_swe", "target_ai",
    "est_hours", "est_hours_beginner",
]  # fmt: skip


def flatten(tree: dict) -> dict[str, tuple[str, str, dict]]:
    """id -> (section_id, module_id, node), in tree order."""
    return {
        sub["id"]: (section["section"]["id"], module["id"], sub)
        for section in tree["sections"]
        for module in section["modules"]
        for sub in module["subtopics"]
    }


def mvp_ids(plan: dict) -> list[str]:
    ids: list[str] = []
    for day in plan["days"][:MVP_LAST_DAY]:
        for sub in day["subtopics"]:
            if not sub["id"].startswith("bh.") and sub["id"] not in ids:
                ids.append(sub["id"])
    return ids


def selected_ids(nodes: dict[str, tuple[str, str, dict]], plan: dict) -> list[str]:
    """The plan-day MVP ids (rule 1), then the extra-track ids in tree order (rule 2)."""
    ids = mvp_ids(plan)
    seen = set(ids)
    for sub_id, (section, module, _) in nodes.items():
        if sub_id not in seen and (section in EXTRA_SECTIONS or module in EXTRA_MODULES):
            ids.append(sub_id)
            seen.add(sub_id)
    return ids


def prerequisites_of(node: dict) -> set[str]:
    lang = node.get("lang_prereqs") or {}
    return set(node.get("prerequisites") or []) | set(lang.get("python") or [])


def build_subtopics(nodes: dict[str, tuple[str, str, dict]], plan: dict) -> list[dict]:
    plan_hours = {k["id"]: k["plan_hours"] for k in plan["selection"]["kept"]}
    first_day: dict[str, int] = {}
    for day in plan["days"][:MVP_LAST_DAY]:
        for sub in day["subtopics"]:
            first_day.setdefault(sub["id"], day["day"])
    subtopics = []
    for position, sub_id in enumerate(selected_ids(nodes, plan), start=1):
        section, module, node = nodes[sub_id]
        subtopics.append(
            {"id": sub_id, "section": section, "module": module}
            | {f: node[f] for f in NODE_FIELDS if f in node}
            | {
                "plan_order": position,
                # Extra-track subtopics are not in the plan days: no plan_day, est_hours as hours.
                "plan_day": first_day.get(sub_id),
                "plan_hours": plan_hours.get(sub_id, node.get("est_hours", 0)),
            }
        )
    return subtopics


def build_assumed(subtopics: list[dict], nodes: dict[str, tuple[str, str, dict]]) -> list[str]:
    """Prerequisites of shipped subtopics that are not themselves shipped (SPEC 5.3 unlock).

    For the curated section/module selection these are simply listed as assumed-known; a prereq
    that is not a real tree node is a data error and fails the sync.
    """
    shipped = {s["id"] for s in subtopics}
    outside = sorted({p for s in subtopics for p in prerequisites_of(s)} - shipped)
    missing = [p for p in outside if p not in nodes]
    if missing:
        raise SystemExit(f"prerequisites not found in the skill tree: {missing}")
    return outside


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("skill_tree", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--out", type=Path, default=CONTENT / "index")
    args = parser.parse_args()

    tree, plan = load_json(args.skill_tree), load_json(args.plan)
    nodes = flatten(tree)
    subtopics = build_subtopics(nodes, plan)

    sd = sum(1 for s in subtopics if s["section"] in EXTRA_SECTIONS)
    ml4 = sum(1 for s in subtopics if s["module"] in EXTRA_MODULES)
    plan_count = len(subtopics) - sd - ml4
    got = (plan_count, sd, ml4, len(subtopics))
    want = (PLAN_MVP_COUNT, EXPECTED_SD, EXPECTED_ML4, EXPECTED_TOTAL)
    if got != want:
        raise SystemExit(
            f"unexpected subtopic counts (plan, sd, ml4, total): got {got}, expected {want}"
        )

    hashes = {"skill_tree.json": sha256_file(args.skill_tree), "plan.json": sha256_file(args.plan)}
    args.out.mkdir(parents=True, exist_ok=True)
    outputs = {
        "subtopics.json": {"source_hash": hashes, "subtopics": subtopics},
        "plan.json": {"source_hash": hashes, "days": plan["days"][:PLAN_SNAPSHOT_LAST_DAY]},
        "assumed.json": {"source_hash": hashes, "assumed": build_assumed(subtopics, nodes)},
    }
    for name, data in outputs.items():
        (args.out / name).write_text(dump_json(data), encoding="utf-8")
    print(f"wrote {', '.join(outputs)} to {args.out} ({len(subtopics)} subtopics)")


if __name__ == "__main__":
    main()
