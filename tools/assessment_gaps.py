"""Content-gap scorecard: per section/module coverage of assessment items and lessons.

Reads files directly (no app imports):
  content/index/subtopics.json, content/placement/*.yaml, content/checks/*.yaml,
  content/lessons/<section>/<subtopic_id>.yaml

Usage: uv run python tools/assessment_gaps.py [--role <swe|ai>-<intern|fresher|junior|senior>]
With --role, also counts role-relevant subtopics (target > 0) and, assuming score 0, the gap total.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from common import CONTENT, load_json, load_yaml

# Item kinds that probe AI-era skills (prompting, LLM evaluation, RAG...). None are authored yet;
# the column stays 0 until such a kind exists, which flags the gap.
AI_ERA_KINDS = frozenset({"prompt_eval", "llm_trace", "rag_design", "ai_review", "ai_debug"})
LEVELS = ("intern", "fresher", "junior", "senior")  # = the tree's `levels` / app LEVELS
ROLES = tuple(f"{track}-{level}" for track in ("swe", "ai") for level in LEVELS)
LEGACY_ROLES = {"swe-new_grad": "swe-fresher", "ai-new_grad": "ai-fresher"}


def _items(path: Path) -> list[dict]:
    data = load_yaml(path) or {}
    return [i for i in data.get("items") or [] if isinstance(i, dict)]


def _item_kinds(directory: Path) -> dict[str, Counter]:
    out: dict[str, Counter] = {}
    for f in sorted(directory.glob("*.yaml")):
        out[f.stem] = Counter(str(i.get("type", "?")) for i in _items(f))
    return out


def _lesson_status(section: str, sid: str) -> str:
    path = CONTENT / "lessons" / section / f"{sid}.yaml"
    if not path.exists():
        return "none"
    return str((load_yaml(path) or {}).get("status", "draft"))


def build_rows(role: str | None) -> list[dict]:
    index = CONTENT / "index" / "subtopics.json"
    if not index.exists():
        raise SystemExit(f"Missing {index} — run `make sync-tree` first.")
    nodes = load_json(index)["subtopics"]
    placement = _item_kinds(CONTENT / "placement")
    checks = _item_kinds(CONTENT / "checks")
    track, _, level = (role or "").partition("-")
    rows: dict[tuple[str, str], dict] = {}
    for n in nodes:
        sid = n["id"]
        r = rows.setdefault(
            (n["section"], n["module"]),
            {
                "section": n["section"],
                "module": n["module"],
                "subtopics": 0,
                "probes": 0,
                "checks": 0,
                "ai_era": 0,
                "published": 0,
                "draft": 0,
                "relevant": 0,
                "gap0": 0,
                "kinds": Counter(),
            },
        )
        r["subtopics"] += 1
        pk, ck = placement.get(sid, Counter()), checks.get(sid, Counter())
        r["probes"] += 1 if sum(pk.values()) else 0
        r["checks"] += 1 if sum(ck.values()) else 0
        r["kinds"].update(pk)
        r["kinds"].update(ck)
        r["ai_era"] += sum(v for k, v in (pk + ck).items() if k in AI_ERA_KINDS)
        status = _lesson_status(n["section"], sid)
        r["published"] += status == "published"
        r["draft"] += status != "published"
        if role:
            target = int((n.get(f"target_{track}") or {}).get(level) or 0)
            r["relevant"] += target > 0
            r["gap0"] += target  # score 0 assumed: gap == target
    return sorted(rows.values(), key=lambda r: (r["section"], r["module"]))


def render(rows: list[dict], role: str | None) -> str:
    cols = [
        ("section", "section"),
        ("module", "module"),
        ("subs", "subtopics"),
        ("probe>=1", "probes"),
        ("check>=1", "checks"),
        ("ai-era", "ai_era"),
        ("lesson pub", "published"),
        ("lesson draft", "draft"),
    ]
    if role:
        cols += [("relevant", "relevant"), ("gap@0", "gap0")]
    total = {k: sum(r[k] for r in rows) for _, k in cols[2:]}
    total.update(section="TOTAL", module="")
    lines_data = [{**r} for r in rows] + [total]
    widths = [max(len(h), *(len(str(r[k])) for r in lines_data)) for h, k in cols]

    def fmt(vals: list[str]) -> str:
        return "| " + " | ".join(v.ljust(w) for v, w in zip(vals, widths, strict=True)) + " |"

    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    out = [sep, fmt([h for h, _ in cols]), sep]
    out += [fmt([str(r[k]) for _, k in cols]) for r in rows]
    out += [sep, fmt([str(total[k]) for _, k in cols]), sep]
    kinds: Counter = Counter()
    for r in rows:
        kinds.update(r["kinds"])
    out.append("Item kinds: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    if total["ai_era"] == 0:
        out.append(
            "FLAG: no AI-era item kind authored yet (" + ", ".join(sorted(AI_ERA_KINDS)) + ")"
        )
    if role:
        out.append(f"Role {role}: gap@0 = sum of targets, assuming every score is 0")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument(
        "--role",
        choices=ROLES + tuple(LEGACY_ROLES),
        help="also count role-relevant subtopics and gap@0",
    )
    args = ap.parse_args()
    role = LEGACY_ROLES.get(args.role, args.role)
    print(render(build_rows(role), role))


if __name__ == "__main__":
    main()
