"""Skill diagnosis (SPEC 5.7): a derived, read-time view over the per-subtopic 0-3 scores.

Pure functions over plain dataclasses (no ORM). It adds no scoring: the result is never an input to
unlock or Leitner.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from .content_loader import SECTION_NAMES, TRACKS, module_name, track_of

LIKELY_KNOWN_SCORE = 2.0
LIKELY_GAP_SCORE = 0.5
MIN_COVERAGE = 0.4
INSUFFICIENT = "Chưa đủ dữ liệu"
BANDS = ((0.75, "Mới"), (1.5, "Cơ bản"), (2.25, "Vững"))
TOP_BAND = "Thành thạo"
TIER_MEASURED, TIER_INFERRED, TIER_NONE = "đã đo", "suy luận", "chưa đo"
STRONG_MAX = 5
IMPROVE_MAX = 5
CONCEPTS_MAX = 3
CONCEPT_LEVEL_ORDER = {"co_ban": 0, "nang_cao": 1}
STALE_DAYS = 180
COVERAGE_WARN_SHARE = 0.5  # warn when more than this share of role-relevant subtopics is unmeasured


@dataclass(frozen=True)
class SubtopicView:
    id: str
    section: str
    module: str
    name_vi: str
    score: int
    measured: bool  # real evidence: score > 0, tested_out, known_basic or a finished lesson
    inferred_hint: str | None = None  # "likely_known" | "likely_gap" (only when not measured)
    has_lesson: bool = False
    concepts: list[str] = field(default_factory=list)
    target: int = 0  # expected 0-3 score for the chosen role; 0 = not role-relevant
    stale: bool = False  # measured, but the last evidence is older than STALE_DAYS


@dataclass
class ModuleDiagnosis:
    module: str
    name_vi: str
    level: str
    mean: float
    coverage: float
    tier: str
    strong: list[dict[str, Any]]
    improve: list[dict[str, Any]]
    not_assessed_count: int
    gap: int = 0
    readiness: float = 0.0
    role_relevant: int = 0
    below_target: int = 0
    unmeasured_relevant: int = 0


@dataclass
class DomainDiagnosis:
    section: str
    name_vi: str
    track: str
    level: str
    mean: float
    coverage: float
    tier: str
    modules: list[ModuleDiagnosis]
    gap: int = 0
    readiness: float = 0.0
    role_relevant: int = 0
    below_target: int = 0
    unmeasured_relevant: int = 0


@dataclass(frozen=True)
class ConceptResult:
    """One answered check item that is tagged with a concept (a CheckResult row, joined)."""

    slug: str
    text: str
    item_id: str
    passed: bool
    item_type: str = ""


def concept_status(results: Iterable[ConceptResult]) -> list[dict[str, Any]]:
    """Per-concept weakness derived from item results (SPEC 5.7). Pure; never feeds score/unlock.

    An item is a hit if it was ever passed, else a miss. `weak` = >= 2 distinct missed items,
    `suspected` = exactly 1 (a lone miss, e.g. one mcq, is never weak). Concepts with only hits
    (ok) or no results (untested) are omitted. Weak first, then by slug."""
    ever: dict[tuple[str, str], bool] = {}
    texts: dict[str, str] = {}
    for r in results:
        key = (r.slug, r.item_id)
        ever[key] = ever.get(key, False) or r.passed
        texts.setdefault(r.slug, r.text)
    counts: dict[str, list[int]] = {}
    for (slug, _item), passed in ever.items():
        counts.setdefault(slug, [0, 0])[0 if passed else 1] += 1
    out = []
    for slug, (n_hit, n_miss) in counts.items():
        if n_miss == 0:
            continue
        status = "weak" if n_miss >= 2 else "suspected"
        out.append(
            {"slug": slug, "text": texts[slug], "status": status, "n_hit": n_hit, "n_miss": n_miss}
        )
    out.sort(key=lambda c: (c["status"] != "weak", c["slug"]))
    return out


def pick_concepts(node: dict[str, Any], limit: int = CONCEPTS_MAX) -> list[str]:
    """Concept texts of an index node: `concepts_vi` basics first, else `key_concepts`."""
    rich = [c for c in node.get("concepts_vi") or [] if c.get("text")]
    if rich:
        rich.sort(key=lambda c: CONCEPT_LEVEL_ORDER.get(c.get("level"), 9))  # stable
        return [c["text"] for c in rich[:limit]]
    return list(node.get("key_concepts") or [])[:limit]


def effective_score(v: SubtopicView) -> float | None:
    """Score used for the mean; None = not assessed (excluded)."""
    if v.measured:
        return float(v.score)
    if v.inferred_hint == "likely_known":
        return LIKELY_KNOWN_SCORE
    if v.inferred_hint == "likely_gap":
        return LIKELY_GAP_SCORE
    return None


def level_of(mean: float, coverage: float) -> str:
    if coverage < MIN_COVERAGE:
        return INSUFFICIENT
    for limit, name in BANDS:
        if mean < limit:
            return name
    return TOP_BAND


def tier_of(measured_count: int, coverage: float, any_inferred: bool) -> str:
    # "đã đo" only once coverage clears the same bar as the level band, so a bucket never shows
    # "đã đo" next to level "Chưa đủ dữ liệu". Below that, any real or inferred signal = "suy luận".
    if coverage >= MIN_COVERAGE:
        return TIER_MEASURED
    if measured_count > 0 or any_inferred:
        return TIER_INFERRED
    return TIER_NONE


def _stats(views: list[SubtopicView]) -> tuple[float, float, str, str]:
    """(mean, coverage, level, tier) of a bucket."""
    total = len(views)
    measured = sum(1 for v in views if v.measured)
    eff = [e for e in (effective_score(v) for v in views) if e is not None]
    mean = sum(eff) / len(eff) if eff else 0.0
    coverage = measured / total if total else 0.0
    any_inferred = any(not v.measured and v.inferred_hint for v in views)
    return mean, coverage, level_of(mean, coverage), tier_of(measured, coverage, any_inferred)


def view_gap(v: SubtopicView) -> int:
    """target - measured for one subtopic; inferred hints never count (real evidence only)."""
    return max(0, v.target - (v.score if v.measured else 0))


def _role_stats(views: list[SubtopicView]) -> dict[str, Any]:
    """Role-relative numbers over role-relevant (target > 0) subtopics only."""
    rel = [v for v in views if v.target > 0]
    target_sum = sum(v.target for v in rel)
    got = sum(min(v.score if v.measured else 0, v.target) for v in rel)
    return {
        "gap": sum(view_gap(v) for v in rel),
        "readiness": round(got / target_sum, 2) if target_sum else 0.0,
        "role_relevant": len(rel),
        # Real-evidence-only, consistent with gap/readiness: an unmeasured or inferred subtopic is
        # "below" (not yet proven at target), so it never contradicts a non-zero gap.
        "below_target": sum(1 for v in rel if (v.score if v.measured else 0) < v.target),
        "unmeasured_relevant": sum(1 for v in rel if not v.measured),
    }


def _is_candidate(v: SubtopicView) -> bool:
    if v.measured:
        return v.score < 2
    return v.inferred_hint == "likely_gap"


def _module(module: str, views: list[SubtopicView], blocking: frozenset[str]) -> ModuleDiagnosis:
    mean, coverage, level, tier = _stats(views)
    strong = sorted((v for v in views if v.measured and v.score >= 2), key=lambda v: -v.score)
    cands = sorted(
        (v for v in views if _is_candidate(v)),
        key=lambda v: (v.id not in blocking, -view_gap(v), not v.measured, v.score),
    )
    improve = [
        {
            "subtopic_id": v.id,
            "name_vi": v.name_vi,
            "score": v.score,
            "state": "measured" if v.measured else "likely_gap",
            "firm": v.measured,
            "concepts": v.concepts[:CONCEPTS_MAX],
            "has_lesson": v.has_lesson,
            "target": v.target,
            "gap": view_gap(v),
            "stale": v.measured and v.stale,
        }
        for v in cands[:IMPROVE_MAX]
    ]
    return ModuleDiagnosis(
        module=module,
        name_vi=module_name(module),
        level=level,
        mean=round(mean, 2),
        coverage=round(coverage, 2),
        tier=tier,
        strong=[
            {"subtopic_id": v.id, "name_vi": v.name_vi, "score": v.score}
            for v in strong[:STRONG_MAX]
        ],
        improve=improve,
        not_assessed_count=sum(1 for v in views if not v.measured and not v.inferred_hint),
        **_role_stats(views),
    )


def _section_order(section: str) -> tuple[int, int]:
    for ti, tr in enumerate(TRACKS):
        if section in tr["sections"]:
            return ti, tr["sections"].index(section)
    return len(TRACKS), 0


def diagnose(
    views: Iterable[SubtopicView],
    *,
    role: str | None = None,
    blocking_ids: frozenset[str] = frozenset(),
) -> list[DomainDiagnosis]:
    """Group views by section then module (input order kept within a section).

    `role` is informational: the per-view `target` is already filled for the chosen role.
    """
    _ = role
    by_section: dict[str, dict[str, list[SubtopicView]]] = {}
    for v in views:
        by_section.setdefault(v.section, {}).setdefault(v.module, []).append(v)
    out = []
    for section in sorted(by_section, key=lambda s: (_section_order(s), s)):
        mods = by_section[section]
        all_views = [v for vs in mods.values() for v in vs]
        mean, coverage, level, tier = _stats(all_views)
        out.append(
            DomainDiagnosis(
                section=section,
                name_vi=SECTION_NAMES.get(section, section),
                track=track_of(section),
                level=level,
                mean=round(mean, 2),
                coverage=round(coverage, 2),
                tier=tier,
                modules=[_module(m, vs, blocking_ids) for m, vs in mods.items()],
                **_role_stats(all_views),
            )
        )
    return out


def readiness_summary(
    domains: list[DomainDiagnosis], views: Iterable[SubtopicView]
) -> dict[str, Any]:
    """Headline over all domains: `readiness_pct` (0-100) and a coverage warning.

    Only real evidence counts. The warning fires when more than half of the role-relevant subtopics
    are unmeasured, and names the domain with the most unmeasured role-relevant subtopics.
    """
    rel = [v for v in views if v.target > 0]
    target_sum = sum(v.target for v in rel)
    got = sum(min(v.score if v.measured else 0, v.target) for v in rel)
    unmeasured = sum(1 for v in rel if not v.measured)
    warn = bool(rel) and unmeasured / len(rel) > COVERAGE_WARN_SHARE
    worst = max(
        (d for d in domains if d.role_relevant > 0),
        key=lambda d: d.unmeasured_relevant / d.role_relevant,  # by share, not raw count
        default=None,
    )
    message = None
    if warn and worst is not None:
        message = f"Phần lớn {worst.name_vi} chưa đo — kết quả còn là ước tính"
    return {
        # None (not 0) when the role has no relevant targets, so the UI can hide a false "0% chuẩn".
        "readiness_pct": round(100 * got / target_sum) if target_sum else None,
        "coverage_warning": warn,
        "coverage_message": message,
        "worst_domain": worst.section if warn and worst is not None else None,
    }
