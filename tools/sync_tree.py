"""Snapshot the parts of skill_tree.json and plan.json the app needs into content/index/.

    uv run python tools/sync_tree.py <skill_tree.json> <plan.json> [--out content/index]

The 40 MVP subtopics are chosen as in SPEC 4.1: ids of plan days 1-12 in plan order, `bh.*`
excluded, each id counted once. Every output file records the sha256 of its source files, so the
committed snapshot shows which version of the sources it was built from (CI cannot read them).
"""

import argparse
from pathlib import Path

from common import CONTENT, dump_json, load_json, sha256_file

MVP_LAST_DAY = 12
PLAN_SNAPSHOT_LAST_DAY = 14
MVP_COUNT = 40

# Node fields the app uses (SPEC 4.2); optional ones are skipped when a node lacks them.
NODE_FIELDS = [
    "name_vi", "order", "summary_vi", "mastery_bar_vi", "prerequisites", "lang_prereqs",
    "key_concepts", "concepts_vi", "examples_vi", "beginner_note_vi", "starter_code_vi",
    "example_problems", "bank_topics", "bank_counts", "target_swe", "target_ai",
    "est_hours", "est_hours_beginner",
]  # fmt: skip


def mvp_ids(plan: dict) -> list[str]:
    ids: list[str] = []
    for day in plan["days"][:MVP_LAST_DAY]:
        for sub in day["subtopics"]:
            if not sub["id"].startswith("bh.") and sub["id"] not in ids:
                ids.append(sub["id"])
    return ids


def prerequisites_of(node: dict) -> set[str]:
    return set(node["prerequisites"]) | set(node["lang_prereqs"]["python"] or [])


def build_subtopics(tree: dict, plan: dict) -> list[dict]:
    nodes = {
        sub["id"]: (section["section"]["id"], module["id"], sub)
        for section in tree["sections"]
        for module in section["modules"]
        for sub in module["subtopics"]
    }
    plan_hours = {k["id"]: k["plan_hours"] for k in plan["selection"]["kept"]}
    first_day = {}
    for day in plan["days"][:MVP_LAST_DAY]:
        for sub in day["subtopics"]:
            first_day.setdefault(sub["id"], day["day"])
    subtopics = []
    for position, sub_id in enumerate(mvp_ids(plan), start=1):
        section, module, node = nodes[sub_id]
        subtopics.append(
            {"id": sub_id, "section": section, "module": module}
            | {f: node[f] for f in NODE_FIELDS if f in node}
            | {
                "plan_order": position,
                "plan_day": first_day[sub_id],
                "plan_hours": plan_hours[sub_id],
            }
        )
    return subtopics


def build_assumed(subtopics: list[dict], plan: dict) -> list[str]:
    in_mvp = {s["id"] for s in subtopics}
    outside = sorted({p for s in subtopics for p in prerequisites_of(s)} - in_mvp)
    known = {a["id"] for a in plan["selection"]["assumed_known"]}
    unplanned = [p for p in outside if p not in known]
    if unplanned:
        raise SystemExit(
            f"prerequisites outside the MVP that the plan does not assume: {unplanned}"
        )
    return outside


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("skill_tree", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--out", type=Path, default=CONTENT / "index")
    args = parser.parse_args()

    tree, plan = load_json(args.skill_tree), load_json(args.plan)
    subtopics = build_subtopics(tree, plan)
    if len(subtopics) != MVP_COUNT:
        raise SystemExit(f"expected {MVP_COUNT} MVP subtopics, found {len(subtopics)}")
    hashes = {"skill_tree.json": sha256_file(args.skill_tree), "plan.json": sha256_file(args.plan)}

    args.out.mkdir(parents=True, exist_ok=True)
    outputs = {
        "subtopics.json": {"source_hash": hashes, "subtopics": subtopics},
        "plan.json": {"source_hash": hashes, "days": plan["days"][:PLAN_SNAPSHOT_LAST_DAY]},
        "assumed.json": {"source_hash": hashes, "assumed": build_assumed(subtopics, plan)},
    }
    for name, data in outputs.items():
        (args.out / name).write_text(dump_json(data), encoding="utf-8")
    print(f"wrote {', '.join(outputs)} to {args.out} ({len(subtopics)} subtopics)")


if __name__ == "__main__":
    main()
