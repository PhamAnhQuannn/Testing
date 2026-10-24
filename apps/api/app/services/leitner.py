"""Leitner 5 boxes (SPEC 5.4), pure. Days are calendar dates in the user's timezone."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

GAP = {1: 1, 2: 2, 3: 4, 4: 7, 5: 14}
GAP_AFTER_BOX5 = 30
MAX_BOX = 5


@dataclass(frozen=True)
class Card:
    box: int
    due_on: date
    lapses: int = 0
    consecutive_passes: int = 0


def gap(new_box: int, *, was_box5: bool = False) -> int:
    """Days to the next review, by the NEW box. A pass while already in box 5 gives 30."""
    if was_box5:
        return GAP_AFTER_BOX5
    return GAP[new_box]


def new_card(event_day: date, offset: int = 0) -> Card:
    """Card created when a subtopic first reaches score >= 1: box 1, due event day + 1.

    `offset` is the placement spread `floor(k / 8)` (SPEC 5.4 rule 1).
    """
    return Card(box=1, due_on=event_day + timedelta(days=1 + offset))


def review(card: Card, success: bool, review_day: date) -> Card:
    """Apply one review done on `review_day` (the real day, so lateness does not pile up debt)."""
    if not success:
        return Card(
            box=1,
            due_on=review_day + timedelta(days=1),
            lapses=card.lapses + 1,
            consecutive_passes=0,
        )
    was5 = card.box >= MAX_BOX
    box = min(card.box + 1, MAX_BOX)
    return Card(
        box=box,
        due_on=review_day + timedelta(days=gap(box, was_box5=was5)),
        lapses=card.lapses,
        consecutive_passes=card.consecutive_passes + 1,
    )


def item_kind_for_box(box: int, *, device_has_editor: bool = True) -> str:
    """Boxes 1-2 use a quick recall item; boxes 3-5 a short code problem when an editor exists."""
    return "code" if box >= 3 and device_has_editor else "recall"
