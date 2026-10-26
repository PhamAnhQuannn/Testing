# Review: py.core.variables_types (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 2 should-fix, 1 Quan pedagogical question)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 72 problems"; `ruff check .` clean; `ruff format --check .` 255 files formatted. 11 blocks; graded: b03, b05, b07, b08 + b09 code_exercise.

## Prereq discipline
- **mastery_check l2 [Q004, X002] is loop-free and conditional-free.** Q004 is `int(x)+2`, `x*2` (read_code); X002 is a tuple swap + `int()` + `type().__name__` (write_code). Neither needs for/if. `checks.pick_item` prefers write_code at level 2, so X002 is what is served; Q004 is only a fallback. Q003 (l1) is fine except the `a = 3; b = 2` semicolon (nit, not taught).
- LC1512 (number-of-good-pairs) is a PRACTICE problem only (`problems.practice`, b10), NOT in mastery_check. It is marked in `statement_vi_md` (needs loops + dict, points to py.core.loops / py.datastructs.dict). OK, but see S2.
- Blocks b01-b09 use only onramp + getting_started concepts. `//` and `**` appear before the operators lesson but each carries a "bài sau sẽ dạy" note (b02, b04). `round(x, 2)` (b06, b07) and `__name__` (b05) are used without introduction (N1).

## Correctness (verified)
- b02 expected_output correct (NoneType class repr, `6 5`, 2**100 = 1267650600228229401496703205376).
- b03 answer c correct, fair distractors. b05 `24 1212 str`, b08 `2 3` correct. b07 answer b correct; the `int()` truncation explanation is accurate.
- Claims OK: int unbounded, strong vs dynamic typing, `int(3.9)==3`, `bool(0/""/None)`, `"5"*2`, `/` always float, 0.1+0.2, `nan != nan`, swap RHS evaluated first. Summary matches body.
- b09 solution `float(p)*int(q)`; expected 10.0/30.0/2.5/0.0 correct.

## Problems / checks
- number-of-good-pairs: bilingual, EN primary, `rewrite_required: true`, expected from solution.py, 11 hidden cases (edge, all-equal, non-adjacent, max). Both wrong/*.py fail (adjacent_only fails s1; off_by_one_count fails h02); the green validator confirms. Adequate.
- check-x002: genuine level-2 write_code, merged into content/checks with problem_id; lesson l2 references it. Solution and tests correct (negatives, leading zero "007", bounds). A solution that skips the swap fails on type names.

## Findings
- **should-fix S1 (X002 shape):** the prompt hands over the swap line and the exact return expression, so it tests transcription more than understanding. Describe the result in words and let the learner write `int(...)`. It also returns a list literal, which this lesson never teaches (only the output shape is given).
- **should-fix S2 (LC1512 placement):** the "needs loops + dict" warning is only in `statement_vi_md`; `statement_en_md` (primary) and the lesson (b10 has no lead-in) say nothing. Add one EN line and a text line before b10 ("bài luyện này cần vòng lặp, làm sau cũng được").
- **nit N1:** introduce `round(x, 2)` and `type(x).__name__` in one phrase at first use (b05 explains after the prediction).
- **nit N2:** b07 distractor c is silly but harmless.
- **nit N3:** Q003 uses `;` on one line.

## Quan question
- Is a `[...]` list literal as a return value in X002/X003 acceptable before lists are taught (output shape only)? Recommended yes, since the prompt states the shape.

## Learner-sim
An (VN, no Python): **4/5**. Friendly, short, good "name tag" mental model, strong float section; loses a point for unexplained `__name__`/`round` and a loop-based practice problem at the end of a day-1 lesson.
