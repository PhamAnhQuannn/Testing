"""Create a draft lesson stub per MVP subtopic from content/index/subtopics.json (T0.4).

    uv run python tools/gen_lesson_stubs.py

Existing lesson files are never overwritten, so authored lessons survive a re-run.
"""

import argparse
import re
from datetime import date
from pathlib import Path

from common import CONTENT, dump_yaml, load_json

STUB_MINUTES = 10
MAX_OBJECTIVES = 4
MIN_FRAGMENT_CHARS = 4
# (separator, minimum sentence length), tried in order until the text yields at least 2 sentences
SPLIT_ATTEMPTS = [(", ", 30), (" và ", 20), (", ", 10), (" và ", 10)]


def split_top_level(text: str, separator: str) -> list[str]:
    """Split on `separator` outside parentheses and quotes."""
    parts, depth, quoted, start = [], 0, False, 0
    for i, ch in enumerate(text):
        if ch == "'":
            quoted = not quoted
        elif not quoted and ch in "([":
            depth += 1
        elif not quoted and ch in ")]":
            depth -= 1
        elif not quoted and depth == 0 and text.startswith(separator, i):
            parts.append(text[start:i])
            start = i + len(separator)
    return [*parts, text[start:]]


def regroup(parts: list[str], joiner: str, min_chars: int) -> list[str]:
    """Merge fragments left to right until each group is long enough to read as a sentence."""
    fragments: list[str] = []
    for part in parts:  # "//, %, ==" must not be cut into one-symbol sentences
        if fragments and len(part) < MIN_FRAGMENT_CHARS:
            fragments[-1] += f"{joiner}{part}"
        else:
            fragments.append(part)
    groups, current = [], ""
    for fragment in fragments:
        current = f"{current}{joiner}{fragment}" if current else fragment
        if len(current) >= min_chars:
            groups.append(current)
            current = ""
    if current:
        if groups:
            groups[-1] += f"{joiner}{current}"
        else:
            groups.append(current)
    return groups


def objectives_from(mastery_bar: str) -> list[str]:
    """Turn "Mức 3: a, b và c." into 2-4 draft sentences (the author agent rewrites them)."""
    text = re.sub(r"^Mức \d:\s*", "", mastery_bar).rstrip(".")
    for separator, min_chars in SPLIT_ATTEMPTS:
        groups = regroup(split_top_level(text, separator), separator, min_chars)
        if len(groups) >= 2:
            break
    else:
        raise ValueError(f"cannot split into objectives: {mastery_bar!r}")
    if len(groups) > MAX_OBJECTIVES:
        groups = [*groups[: MAX_OBJECTIVES - 1], ", ".join(groups[MAX_OBJECTIVES - 1 :])]
    cleaned = [re.sub(r"^và\s+", "", g.strip()) for g in groups]
    return [g[:1].upper() + g[1:] + "." for g in cleaned]


def build_stub(subtopic: dict, tree_hash: str, today: str) -> dict:
    return {
        "id": subtopic["id"],
        "version": 1,
        "status": "draft",
        "title_vi": subtopic["name_vi"],
        "est_minutes": STUB_MINUTES,
        "objectives_vi": objectives_from(subtopic["mastery_bar_vi"]),
        "blocks": [],
        "problems": {"practice": [], "extra": []},
        "mastery_check": {"l1": [], "l2": [], "l3": []},
        "checkpoint": {"pass_ratio": 0.7, "min_items": 3},
        "source": {
            "tree_hash": tree_hash,
            "authored_by": "tools/gen_lesson_stubs.py",
            "reviewed_by": None,
            "date": today,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--content", type=Path, default=CONTENT)
    args = parser.parse_args()

    index = load_json(args.content / "index" / "subtopics.json")
    tree_hash = index["source_hash"]["skill_tree.json"]
    today = date.today().isoformat()
    created = 0
    for subtopic in index["subtopics"]:
        path = args.content / "lessons" / subtopic["section"] / f"{subtopic['id']}.yaml"
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(dump_yaml(build_stub(subtopic, tree_hash, today)), encoding="utf-8")
        created += 1
    print(f"created {created} lesson stubs, kept {len(index['subtopics']) - created} existing")


if __name__ == "__main__":
    main()
