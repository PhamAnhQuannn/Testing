"""Unlock rule (SPEC 5.3), pure. `unlocked_at` is one-way: once set it is never cleared."""

from __future__ import annotations

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from datetime import datetime

from .scoring import is_done

LOCKED = "locked"
UNLOCKED = "unlocked"
IN_PROGRESS = "in_progress"
DONE = "done"
BLOCKED_MISSING_CONTENT = "blocked_missing_content"


@dataclass(frozen=True)
class Unlock:
    unlocked: bool
    reasons: tuple[dict, ...] = ()  # one entry per unmet prerequisite
    blocked_missing_content: bool = False


def evaluate(
    prereqs: Collection[str],
    assumed: Collection[str],
    content_ids: Collection[str],
    scores: Mapping[str, int],
    unlocked_at: datetime | None = None,
) -> Unlock:
    """unlocked_at set, or every prerequisite assumed / in content with score >= 2."""
    if unlocked_at is not None:
        return Unlock(True)
    reasons: list[dict] = []
    missing = False
    for p in prereqs:
        if p in assumed:
            continue
        if p not in content_ids:
            missing = True
            reasons.append({"prerequisite": p, "score": None, "need": 2, "missing_content": True})
            continue
        s = scores.get(p, 0)
        if s < 2:
            reasons.append({"prerequisite": p, "score": s, "need": 2})
    return Unlock(not reasons, tuple(reasons), missing)


def newly_unlocked(
    result: Unlock, unlocked_at: datetime | None, now: datetime, *, tested_out: bool = False
) -> datetime | None:
    """New value of `unlocked_at`: unchanged if already set, `now` the first time it is true.

    `tested_out` also unlocks the subtopic itself (SPEC 5.3).
    """
    if unlocked_at is not None:
        return unlocked_at
    if result.unlocked or tested_out:
        return now
    return None


def status(
    unlocked: bool,
    score_value: int,
    target_intern: int,
    *,
    has_activity: bool,
    blocked_missing_content: bool = False,
) -> str:
    if not unlocked:
        return BLOCKED_MISSING_CONTENT if blocked_missing_content else LOCKED
    if is_done(score_value, target_intern):
        return DONE
    if has_activity or score_value > 0:
        return IN_PROGRESS
    return UNLOCKED
