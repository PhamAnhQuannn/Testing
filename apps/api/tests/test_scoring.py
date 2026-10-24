"""SPEC 5.2: the three worked examples, edge cases, unlock (5.3) and Leitner (5.4)."""

from datetime import date, datetime

import pytest

from app.services import leitner, unlock
from app.services import scoring as sc

DICT = sc.SubtopicSpec(
    practice_ids=("ransom-note",),
    graded_quiz_ids=tuple(f"d#q{i}" for i in range(1, 6)),
    has_l2_items=True,
    has_l3_write_code=True,
)


def answers(run: int, correct: list[bool], prefix: str = "d") -> tuple[sc.QuizAnswerEv, ...]:
    return tuple(sc.QuizAnswerEv(f"{prefix}#q{i + 1}", run, 1, ok) for i, ok in enumerate(correct))


# ---- quiz_best ----


def test_quiz_best_first_answer_only_and_best_run():
    ans = (
        sc.QuizAnswerEv("d#q1", 1, 1, False),
        sc.QuizAnswerEv("d#q1", 1, 2, True),  # a retry in the same run does not count
        sc.QuizAnswerEv("d#q2", 1, 1, True),
        sc.QuizAnswerEv("d#q3", 1, 1, True),
        sc.QuizAnswerEv("d#q1", 2, 1, True),
        sc.QuizAnswerEv("d#q2", 2, 1, True),
        sc.QuizAnswerEv("d#q3", 2, 1, True),
    )
    assert sc.quiz_best(ans, ["d#q1", "d#q2", "d#q3"]) == 1.0  # run 2
    assert sc.quiz_best(
        [a for a in ans if a.run_no == 1], ["d#q1", "d#q2", "d#q3"]
    ) == pytest.approx(2 / 3)


def test_quiz_best_needs_min_items_and_ignores_ungraded():
    ans = answers(1, [True, True])
    assert sc.quiz_best(ans, ["d#q1", "d#q2", "d#q3"]) is None
    ans = answers(1, [True, True, True])
    assert sc.quiz_best(ans, ["d#q1", "d#q2"]) is None  # q3 is not graded
    assert sc.quiz_best((), ["d#q1"]) is None


# ---- worked example 1: normal path, earliest score 3 ----


def test_example_1_normal_path():
    quiz = answers(1, [True, True, True, True, False])  # 4/5 = 0.8
    ev = sc.Evidence(lesson_done=True, quiz_answers=quiz)
    assert sc.score(DICT, ev).score == 1
    assert sc.score(DICT, ev).quiz_best == pytest.approx(0.8)

    ac = sc.AttemptEv("ransom-note", ac=True, clean=True)
    ev = sc.Evidence(True, quiz, (ac,))
    r = sc.score(DICT, ev)
    assert r.practice_ok and r.score == 1  # still 1: no check yet

    q23 = sc.CheckEv("Q023", 2, passed=True, clean=True)
    ev = sc.Evidence(True, quiz, (ac,), (q23,))
    r = sc.score(DICT, ev)
    assert r.tested_out and r.check2_ok and r.s2 and r.score == 2

    q24 = sc.CheckEv("Q024", 3, passed=True, clean=True, item_type="write_code")
    ev = sc.Evidence(True, quiz, (ac,), (q23, q24))
    r = sc.score(DICT, ev)
    assert r.level3_ok and not r.retention_ok and r.score == 2

    # review log: day 3 (box 1), day 5 (box 2), day 9 (box 3, a code item)
    reviews = (
        sc.ReviewEv(True, 1, "recall"),
        sc.ReviewEv(True, 2, "recall"),
        sc.ReviewEv(True, 3, "code"),
    )
    ev = sc.Evidence(True, quiz, (ac,), (q23, q24), reviews)
    assert sc.score(DICT, ev).score == 3

    # a recall card in box 3 moves the card up but is not retention evidence
    recall = reviews[:2] + (sc.ReviewEv(True, 3, "recall"),)
    ev = sc.Evidence(True, quiz, (ac,), (q23, q24), recall)
    assert sc.score(DICT, ev).score == 2


def test_example_1_leitner_dates():
    day = lambda n: date(2026, 11, n)  # noqa: E731
    card = leitner.new_card(day(2))
    assert (card.box, card.due_on) == (1, day(3))
    card = leitner.review(card, True, day(3))
    assert (card.box, card.due_on) == (2, day(5))
    card = leitner.review(card, True, day(5))
    assert (card.box, card.due_on) == (3, day(9))  # D+7
    card = leitner.review(card, True, day(9))
    assert (card.box, card.due_on) == (4, day(16))  # D+14
    card = leitner.review(card, True, day(16))
    assert (card.box, card.due_on) == (5, day(30))  # D+28
    card = leitner.review(card, True, day(30))
    assert (card.box, card.due_on) == (5, date(2026, 12, 30))  # then +30


# ---- worked example 2: test out ----


def test_example_2_test_out_gives_2_without_lesson():
    spec = sc.SubtopicSpec(practice_ids=("p1", "p2"), has_l2_items=True, has_l3_write_code=True)
    ev = sc.Evidence(checks=(sc.CheckEv("Q1", 2, True, True),))
    r = sc.score(spec, ev)
    assert (r.score, r.s1, r.tested_out) == (2, False, True)
    # still needs level 3 write_code and a code review at box >= 3 for the third point
    ev = sc.Evidence(
        checks=(
            sc.CheckEv("Q1", 2, True, True),
            sc.CheckEv("Q2", 3, True, True, item_type="concept"),
        ),
        reviews=(sc.ReviewEv(True, 3, "code"),),
    )
    assert sc.score(spec, ev).score == 2  # a concept item is not level-3 evidence
    ev = sc.Evidence(
        checks=(sc.CheckEv("Q1", 2, True, True), sc.CheckEv("Q2", 3, True, True)),
        reviews=(sc.ReviewEv(True, 3, "code"),),
    )
    assert sc.score(spec, ev).score == 3
    # test out, new card due the day after
    assert leitner.new_card(date(2026, 11, 6)).due_on == date(2026, 11, 7)


# ---- worked example 3: fail, then still progress via the exit ----


def test_example_3_failed_l2_exit():
    spec = sc.SubtopicSpec(
        practice_ids=("p1", "p2"),
        graded_quiz_ids=("d#q1", "d#q2", "d#q3"),
        has_l2_items=True,
    )
    quiz = answers(1, [True, True, True])
    fail = sc.CheckEv("Q1", 2, passed=False)
    p1 = sc.AttemptEv("p1", ac=True, clean=True)
    p2 = sc.AttemptEv("p2", ac=True, clean=False)  # practice needs only a plain AC

    # one clean AC is not enough: two distinct practice problems are needed
    r = sc.score(spec, sc.Evidence(True, quiz, (p1,), (fail,)))
    assert not r.practice_ok and r.score == 1
    r = sc.score(spec, sc.Evidence(True, quiz, (p1, p2), (fail,)))
    assert r.practice_ok and r.check2_ok and r.score == 2
    # no failed check, no exit
    r = sc.score(spec, sc.Evidence(True, quiz, (p1, p2), ()))
    assert not r.check2_ok and r.score == 1
    # giving up is not a failure
    r = sc.score(
        spec, sc.Evidence(True, quiz, (p1, p2), (sc.CheckEv("Q1", 2, False, gave_up=True),))
    )
    assert not r.check2_ok
    # the exit needs a *clean* practice AC
    r = sc.score(spec, sc.Evidence(True, quiz, (sc.AttemptEv("p1", True, False), p2), (fail,)))
    assert not r.check2_ok
    # a retry that passes later also works
    r = sc.score(spec, sc.Evidence(True, quiz, (), (fail, sc.CheckEv("Q1", 2, True, True))))
    assert r.score == 2


# ---- edge cases ----


def test_unclean_check_pass_is_no_evidence():
    r = sc.score(DICT, sc.Evidence(checks=(sc.CheckEv("Q", 2, True, clean=False),)))
    assert r.score == 0 and not r.tested_out


def test_lesson_done_needs_quiz_and_vice_versa():
    quiz = answers(1, [True] * 5)
    assert sc.score(DICT, sc.Evidence(False, quiz)).score == 0
    assert sc.score(DICT, sc.Evidence(True, ())).score == 0
    bad = answers(1, [True, False, False, False, False])
    assert sc.score(DICT, sc.Evidence(True, bad)).score == 0
    boundary = answers(1, [True, True, True, False, False, False, False][:3])  # 3/3
    assert sc.score(DICT, sc.Evidence(True, boundary)).score == 1


def test_practice_ok_edge_cases():
    quiz = answers(1, [True] * 5)
    none = sc.SubtopicSpec(graded_quiz_ids=DICT.graded_quiz_ids)
    r = sc.score(none, sc.Evidence(True, quiz))
    assert r.practice_ok and r.check2_ok and r.score == 2  # nothing to demand
    # only the practice problems of the lesson count, extras do not
    r = sc.score(DICT, sc.Evidence(True, quiz, (sc.AttemptEv("extra", True, True),)))
    assert not r.practice_ok
    # two attempts at the same problem are one problem
    two = sc.SubtopicSpec(practice_ids=("a", "b"), graded_quiz_ids=DICT.graded_quiz_ids)
    ev = sc.Evidence(True, quiz, (sc.AttemptEv("a", True, True), sc.AttemptEv("a", True, True)))
    assert not sc.score(two, ev).practice_ok


def test_check2_without_l2_items_needs_clean_practice():
    spec = sc.SubtopicSpec(practice_ids=("p",), graded_quiz_ids=DICT.graded_quiz_ids)
    quiz = answers(1, [True] * 5)
    assert sc.score(spec, sc.Evidence(True, quiz, (sc.AttemptEv("p", True, False),))).score == 1
    assert sc.score(spec, sc.Evidence(True, quiz, (sc.AttemptEv("p", True, True),))).score == 2


def test_level3_fallbacks():
    quiz = answers(1, [True] * 5)
    ret = (sc.ReviewEv(True, 3, "code"),)
    base = dict(graded_quiz_ids=DICT.graded_quiz_ids, practice_ids=("p",))
    # no write_code L3 item, a medium practice problem: needs a clean AC on it
    spec = sc.SubtopicSpec(medium_practice_ids=("p",), **base)
    ev = sc.Evidence(True, quiz, (sc.AttemptEv("p", True, False),), reviews=ret)
    assert sc.score(spec, ev).score == 1  # unclean AC: check2 (no L2 item) fails too
    ev = sc.Evidence(True, quiz, (sc.AttemptEv("p", True, True),), reviews=ret)
    assert sc.score(spec, ev).score == 3
    # nothing at all for level 3: true
    spec = sc.SubtopicSpec(**base)
    assert sc.score(spec, ev).level3_ok


def test_retention_rules():
    quiz = answers(1, [True] * 5)
    ac = sc.AttemptEv("ransom-note", True, True)
    chk = (sc.CheckEv("Q23", 2, True, True), sc.CheckEv("Q24", 3, True, True))

    def s(*reviews):
        return sc.score(DICT, sc.Evidence(True, quiz, (ac,), chk, reviews)).score

    assert s(sc.ReviewEv(True, 2, "code")) == 2  # box_before < 3
    assert s(sc.ReviewEv(False, 3, "code")) == 2  # failed
    assert s(sc.ReviewEv(True, 4, "code")) == 3
    assert s(sc.ReviewEv(True, 3, "recall")) == 2


def test_no_decay_and_is_done():
    assert sc.is_done(1, 0) and not sc.is_done(0, 0)  # target 0 still needs score 1
    assert sc.is_done(2, 2) and not sc.is_done(1, 2) and sc.is_done(1, 1)


# ---- leitner ----


def test_leitner_fail_and_box5():
    card = leitner.Card(box=4, due_on=date(2026, 1, 1), lapses=1, consecutive_passes=3)
    failed = leitner.review(card, False, date(2026, 1, 10))
    assert (failed.box, failed.due_on, failed.lapses, failed.consecutive_passes) == (
        1,
        date(2026, 1, 11),
        2,
        0,
    )
    assert [leitner.gap(b) for b in (1, 2, 3, 4, 5)] == [1, 2, 4, 7, 14]
    assert leitner.gap(5, was_box5=True) == 30
    # late review: the next date counts from the real day, no debt
    late = leitner.review(leitner.Card(1, date(2026, 1, 2)), True, date(2026, 1, 20))
    assert late.due_on == date(2026, 1, 22)
    assert leitner.new_card(date(2026, 1, 1), offset=2).due_on == date(2026, 1, 4)
    assert leitner.item_kind_for_box(2) == "recall"
    assert leitner.item_kind_for_box(3) == "code"
    assert leitner.item_kind_for_box(3, device_has_editor=False) == "recall"


# ---- unlock ----

NOW = datetime(2026, 1, 1).astimezone()


def test_unlock_rules():
    ok = unlock.evaluate(["a", "assumed"], {"assumed"}, {"a", "b"}, {"a": 2})
    assert ok.unlocked
    low = unlock.evaluate(["a"], set(), {"a"}, {"a": 1})
    assert not low.unlocked and low.reasons[0]["score"] == 1
    missing = unlock.evaluate(["zzz"], set(), {"a"}, {})
    assert not missing.unlocked and missing.blocked_missing_content
    # one-way: once unlocked_at is set a lower score never locks again
    assert unlock.evaluate(["a"], set(), {"a"}, {"a": 0}, unlocked_at=NOW).unlocked
    assert unlock.newly_unlocked(low, None, NOW) is None
    assert unlock.newly_unlocked(ok, None, NOW) == NOW
    assert unlock.newly_unlocked(low, None, NOW, tested_out=True) == NOW
    earlier = datetime(2025, 1, 1).astimezone()
    assert unlock.newly_unlocked(ok, earlier, NOW) == earlier


def test_status():
    s = unlock.status
    assert s(False, 0, 2, has_activity=False) == "locked"
    assert (
        s(False, 0, 2, has_activity=False, blocked_missing_content=True)
        == "blocked_missing_content"
    )
    assert s(True, 0, 2, has_activity=False) == "unlocked"
    assert s(True, 1, 2, has_activity=True) == "in_progress"
    assert s(True, 2, 2, has_activity=True) == "done"
    assert s(True, 1, 1, has_activity=True) == "done"  # memory_model style: target 1
    assert s(True, 0, 0, has_activity=False) == "unlocked"  # optional item at 0 is not done
    assert s(True, 1, 0, has_activity=True) == "done"
