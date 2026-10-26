# Review: py.core.operators (reviewer pass, independent)

**Verdict: CHANGES-NEEDED** (1 blocker in the check pool; the lesson text itself is clean)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 72 problems"; `ruff check .` clean; `ruff format --check .` 255 files formatted. 11 blocks; graded: b03, b06, b08 + b09 code_exercise.

## BLOCKER
- **B1 - Q006 (`digit_sum`, level 2, write_code) is served ahead of X003 and requires a `while` loop.** `content/checks/py.core.operators.yaml` lists Q006 then X003, both write_code at difficulty 2. `ContentStore.check_items` ignores the lesson's `mastery_check` lists (the lesson only references X003), and `checks.pick_item` takes `group[(attempt_no-1) % len]`, so the FIRST level-2 attempt is Q006; X003 only appears on a redo. Q006 ("KHÔNG đổi sang chuỗi, dùng // và %") cannot be solved without a loop, which is not taught yet. This violates the prereq bar at the real gate (check-q006 solution uses `while`). Fix options (outside this review): make `convert_checks`/checks_extra drop or demote Q006 for this subtopic, or have `pick_item` honor the lesson's `mastery_check.l2` list/order. After the fix, verify only X003 is reachable at level 2. The same pattern may hit other lessons: grep all generated write_code check items for un-taught concepts.

## Prereq discipline (lesson)
- mastery_check l2 [X003] is loop-free and conditional-free: two `divmod`s returning a list; the statement says "không cần vòng lặp". Q005 (l1) is plain arithmetic.
- LC1281 (subtract-product-and-sum) is practice only (`problems.practice`, b10), NOT a gate. `statement_vi_md` says it needs a `while` loop taught later; the reference solution uses while (allowed for practice). The EN statement lacks the note (S1).
- Blocks use `and/or/not`, comparisons and `is None` without if/else; no loops/lists/dicts. The b07 one-liner on bit ops, Decimal, Fraction, random is "look up later": fine.

## Correctness (verified)
- b02, b03, b05, b08 outputs correct: `-7//2=-4`, `-7%3=2`, `(3-5)%24=22`, `-17//5,-17%5 = -4 3`, `17//-5,17%-5 = -4 -3`, `-2**2=-4`, `2**3**2=512`, x chain 15, 30, 7, round(2.5)=2, round(3.5)=4, isqrt(17)=4, gcd 6, floor/ceil(-2.5) = -3/-2.
- Claims accurate: `%` takes the sign of the divisor, `a == (a//b)*b + a%b`, banker's rounding, `round(2.675, 2) == 2.67`, `==` vs `is`, short-circuit and operand-returning and/or, chained comparison, precedence order.
- b06 answer b (14) correct. Distractor c "64: left to right" is wrong as stated (left to right gives 100): nit N1.
- b09 `(hour+add) % 24`: tests 3, 22, 0, 0 correct.

## Problems / checks
- subtract-product-and-sum: bilingual, EN primary, `rewrite_required: true`, expected from solution.py, 11 hidden (zero digits, max 100000, single digit). wrong/product_starts_zero and wrong/reversed_sign both fail s1 and hidden (green validator confirms). Adequate.
- check-x003: genuine write_code, correct solution; 9 hidden cover 0, 59, 60, 3599, 3600, 86399, 100000. Merged into content/checks with problem_id; lesson l2 references it.

## Findings
- **blocker B1:** above.
- **should-fix S1:** add the "needs a while loop, learn later" note to `statement_en_md` of LC1281 and a one-line lead-in before b10.
- **nit N1:** b06 distractor c value (use 100).
- **nit N2:** b01 packs divmod and negative floor semantics into a dense paragraph; consider a separate short block for the negative-number part.

## Learner-sim
An (VN, no Python): **3.5/5**. Text is clear and well ordered (clock-wrap is a nice hook), but a first-attempt mastery check that demands a loop would stall An; expect 4/5 once B1 is fixed.
