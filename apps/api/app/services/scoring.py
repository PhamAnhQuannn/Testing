"""Score 0-3 of one subtopic, a pure function of the event tables (SPEC 5.2).

Nothing here touches the database: callers load the events and the content facts and pass them in.
`user_subtopic.score` is only a cache of `score()`.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

PASS_RATIO = 0.7
MIN_ITEMS = 3
GRADED_QUIZ_PASS = PASS_RATIO


@dataclass(frozen=True)
class QuizAnswerEv:
    quiz_item_id: str
    run_no: int
    attempt_no: int
    correct: bool


@dataclass(frozen=True)
class AttemptEv:
    """A Submit attempt. Only `ac` ones matter; `clean` is decided when the attempt is recorded."""

    problem_id: str
    ac: bool
    clean: bool


@dataclass(frozen=True)
class CheckEv:
    item_id: str
    level: int
    passed: bool
    clean: bool = False
    gave_up: bool = False
    # write_code | read_code | concept | mcq score; write_test is diagnostic-only (the learner
    # writes a test that catches a planted bug): it never gates a score, a level or a lock.
    item_type: str = "write_code"
    context: str = "mastery"  # mastery | test_out | placement


@dataclass(frozen=True)
class ReviewEv:
    success: bool
    box_before: int
    item_kind: str  # code | recall


@dataclass(frozen=True)
class SubtopicSpec:
    """Content facts about the subtopic that the rules need."""

    practice_ids: tuple[str, ...] = ()
    medium_practice_ids: tuple[str, ...] = ()
    graded_quiz_ids: tuple[str, ...] = ()
    has_l2_items: bool = False
    has_l3_write_code: bool = False
    # Concept subtopic (SPEC 5.2): no practice problem and no `write_code` check item at any
    # level (System Design + the AI-engineer LLM track). Its score-2/3 evidence is a clean
    # `concept`/`read_code` check pass, and review retention may be earned with a recall item.
    is_concept: bool = False
    has_l3_items: bool = False  # any level-3 check item (any type), for the concept level-3 gate
    pass_ratio: float = PASS_RATIO
    min_items: int = MIN_ITEMS


@dataclass(frozen=True)
class Evidence:
    lesson_done: bool = False
    quiz_answers: tuple[QuizAnswerEv, ...] = ()
    attempts: tuple[AttemptEv, ...] = ()
    checks: tuple[CheckEv, ...] = ()
    reviews: tuple[ReviewEv, ...] = ()


@dataclass(frozen=True)
class ScoreResult:
    score: int
    s1: bool
    s2: bool
    s3: bool
    tested_out: bool
    tested_basic: bool
    quiz_best: float | None
    practice_ok: bool
    check2_ok: bool
    level3_ok: bool
    retention_ok: bool
    flags: dict[str, bool] = field(default_factory=dict)


def quiz_best(
    answers: Iterable[QuizAnswerEv],
    graded_ids: Iterable[str],
    min_items: int = MIN_ITEMS,
) -> float | None:
    """Best run ratio, counting only the first answer of each graded block within a run.

    A run needs at least `min_items` answered graded blocks to count (SPEC 5.1). The ratio is
    correct first answers / ALL graded blocks of the lesson: an unanswered block counts as wrong.
    None when no run qualifies.
    """
    graded = set(graded_ids)
    first: dict[tuple[int, str], QuizAnswerEv] = {}
    for a in answers:
        if a.quiz_item_id not in graded:
            continue
        key = (a.run_no, a.quiz_item_id)
        cur = first.get(key)
        if cur is None or a.attempt_no < cur.attempt_no:
            first[key] = a
    per_run: dict[int, list[bool]] = defaultdict(list)
    for (run_no, _), a in first.items():
        per_run[run_no].append(a.correct)
    best: float | None = None
    for results in per_run.values():
        if len(results) < min_items:
            continue
        ratio = sum(results) / len(graded)
        if best is None or ratio > best:
            best = ratio
    return best


def _check_pass(checks: Iterable[CheckEv], level: int, item_type: str | None = None) -> bool:
    return any(
        c.item_type != "write_test"
        and c.level == level
        and c.passed
        and c.clean
        and (item_type is None or c.item_type == item_type)
        for c in checks
    )


def score(spec: SubtopicSpec, ev: Evidence) -> ScoreResult:
    best = quiz_best(ev.quiz_answers, spec.graded_quiz_ids, spec.min_items)
    s1 = ev.lesson_done and best is not None and best >= spec.pass_ratio
    tested_out = _check_pass(ev.checks, 2)
    # Placement redesign (SPEC 5.6): a clean level-1 KEYED pass (mcq or read_code, objectively
    # machine-graded) IN A PLACEMENT sitting proves basic knowledge = score 1. A self-graded
    # `concept` pass never does, and this is PLACEMENT-ONLY: a level-1 read_code diagnostic reached
    # in a mastery/test_out ladder (only after an L2 write_code fail) must NOT mark the subtopic
    # score 1 / "done" — the mastery score-2 bar still rests on measured code there.
    tested_basic = any(
        c.item_type != "write_test"
        and c.level == 1
        and c.passed
        and c.clean
        and c.context == "placement"
        and c.item_type in ("mcq", "read_code")
        for c in ev.checks
    )

    practice = set(spec.practice_ids)
    ac_practice = {a.problem_id for a in ev.attempts if a.ac and a.problem_id in practice}
    clean_practice = {
        a.problem_id for a in ev.attempts if a.ac and a.clean and a.problem_id in practice
    }
    need = min(2, len(practice))
    practice_ok = len(ac_practice) >= need  # no practice problems: need = 0, so true

    if tested_out:
        check2_ok = True
    elif spec.has_l2_items:
        failed_l2 = any(
            c.level == 2 and not c.passed and not c.gave_up and c.item_type != "write_test"
            for c in ev.checks
        )
        check2_ok = failed_l2 and bool(clean_practice) and len(ac_practice) >= need
    elif practice:
        check2_ok = bool(clean_practice)
    else:
        check2_ok = True  # nothing to demand (no L2 item, no practice problem)

    s2 = tested_out or (s1 and practice_ok and check2_ok)

    medium = set(spec.medium_practice_ids)
    if spec.has_l3_write_code:
        level3_ok = _check_pass(ev.checks, 3, "write_code")
    elif spec.is_concept and spec.has_l3_items:
        # Concept subtopic: a clean level-3 concept/read_code pass is the interview-level gate
        # (mirrors the `big_o` no-write_code fallback; True only when no L3 item was authored).
        level3_ok = _check_pass(ev.checks, 3)
    elif medium:
        level3_ok = any(a.ac and a.clean and a.problem_id in medium for a in ev.attempts)
    else:
        level3_ok = True

    # A recall review counts for retention only on a concept subtopic (SPEC 5.2); code subtopics
    # still require a code review at box >= 3, so the existing 40 py/dsa/cs are unchanged.
    retention_ok = any(
        r.success and r.box_before >= 3 and (r.item_kind == "code" or spec.is_concept)
        for r in ev.reviews
    )
    s3 = s2 and level3_ok and retention_ok

    if s3:
        value = 3
    elif s2:
        value = 2
    elif s1 or tested_out or tested_basic:
        value = 1
    else:
        value = 0
    return ScoreResult(
        score=value,
        s1=s1,
        s2=s2,
        s3=s3,
        tested_out=tested_out,
        tested_basic=tested_basic,
        quiz_best=best,
        practice_ok=practice_ok,
        check2_ok=check2_ok,
        level3_ok=level3_ok,
        retention_ok=retention_ok,
    )


def is_done(score_value: int, target_intern: int) -> bool:
    """done = score >= max(1, target_intern) (SPEC 5.3)."""
    return score_value >= max(1, target_intern)
