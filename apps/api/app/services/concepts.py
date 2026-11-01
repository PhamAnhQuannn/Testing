"""Concept slugs: the single definition shared by the API and the content validator.

Stdlib only on purpose: tools/validate_content.py imports it without the API's dependencies.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

_PAREN = re.compile(r"\([^)]*\)")
_NON_SLUG = re.compile(r"[^a-z0-9]+")
SLUG_MAX = 40


def _fold(text: str) -> str:
    """ASCII-fold accents so VN keeps its letters: 'Vòng lặp' -> 'vong lap', not 'v ng l p'."""
    nfkd = unicodedata.normalize("NFKD", text)
    stripped = "".join(c for c in nfkd if not unicodedata.combining(c))
    return stripped.replace("đ", "d").replace("Đ", "D")


def slugify(text: str) -> str:
    """Lowercase + ASCII-fold, drop `(...)`, collapse non [a-z0-9] to `-`, cap SLUG_MAX."""
    folded = _fold(text.lower())
    s = _NON_SLUG.sub("-", _PAREN.sub(" ", folded)).strip("-")
    return s[:SLUG_MAX].strip("-")


def registry_of(node: dict[str, Any]) -> dict[str, str]:
    """{slug: text} of an index node: `concepts_vi` texts (preferred), else `key_concepts`."""
    texts = [c["text"] for c in node.get("concepts_vi") or [] if c.get("text")]
    if not texts:
        texts = [x for x in node.get("key_concepts") or [] if isinstance(x, str)]
    out: dict[str, str] = {}
    for text in texts:
        slug = slugify(text)
        if slug:
            out.setdefault(slug, text)
    return out


def registry_problems(node: dict[str, Any]) -> list[str]:
    """Collisions / empty slugs in a node's concept list. A tagged subtopic with any of these would
    make a concept untaggable or map a tag to the wrong text, so the validator fails the build."""
    texts = [c["text"] for c in node.get("concepts_vi") or [] if c.get("text")]
    if not texts:
        texts = [x for x in node.get("key_concepts") or [] if isinstance(x, str)]
    seen: dict[str, str] = {}
    problems: list[str] = []
    for text in texts:
        slug = slugify(text)
        if not slug:
            problems.append(f"concept {text!r} has an empty slug (unsluggable text)")
        elif slug in seen and seen[slug] != text:
            problems.append(f"slug {slug!r} collides: {seen[slug]!r} vs {text!r}")
        else:
            seen.setdefault(slug, text)
    return problems


# Cross-cutting work practices an item can be tagged with (fixed vocabulary, no registry).
PRACTICES = ("verify", "review", "measure")
PRACTICE_LABELS = {
    "verify": "Kiểm chứng đầu ra (bắt bug, nhất là code AI viết)",
    "review": "Đọc & review code",
    "measure": "Đo lường & eval (precision/recall…)",
}
