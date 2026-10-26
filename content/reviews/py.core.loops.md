# Review: py.core.loops (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 1 should-fix)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 76 problems"; `ruff check .` clean. 11 blocks; graded: b04, b06, b07, b08, b09 (code_exercise).

## Prereq discipline (key)
- `mastery_check: l1 [Q009], l2 [Q010]`; the generated pool for loops has only Q009 and Q010, so the list is complete and honored.
- Q009 (`range(2,10,3)` read_code): pure taught content. Q010 (`count_vowels`, 'Interview' -> 4) is solvable with `for ch in s` + `if ch in "aeiou"` + counter: all taught in conditionals/loops. The reference uses `.lower()` (taught next lesson); a learner can instead use `ch in "aeiouAEIOU"` (hidden tests include 'AEIOU', 'AeIoU xyz'). No lists needed. Solvable, but see S1.
- ugly-number is practice only (b10): uses `for`, `while`, `//=`, `%`, tuple `(2, 3, 5)` in solution (all loops-lesson content). It needs only this lesson, so no "taught later" note is needed. Not a gate.
- Previews: tuple `(2, 3, 5)` as "dãy giá trị cố định, list/tuple học ở py.datastructs" (b01/b02) is acceptable: one clause, used only as an iterable. No list operations anywhere. `end=","` was taught in getting_started.

## Correctness (verified by hand)
- b02: 15; digits of "py3.12" -> `3,1,2,`; squares `4,9,25,`. b04: `10,7,4,1,` and 10. b06: range(3,12,4) = 3,7,11 (b). b07 (a) correct incl. empty sequence. b08 nested output `2 1 / 2 3 / 3 1` traced correct.
- Prose: continue sum = 27; primes loop prints `2,3,5,7,` (range(2,2) empty, so else runs); digit-sum example 15; `range(10**9)` lazy claim correct; break/continue affect innermost loop only. Collatz tests 1->0, 2->1, 6->8, 7->16, 27->111 correct.
- ugly-number: bilingual, rewrite_required true; wrong/missing_five (fails 5/25/30), one_is_not_ugly (fails 1), single_pass (fails 8) each fail hidden (green validator confirms); hidden covers 1, 0, negatives, primes, 2^30, INT_MAX, INT_MIN, 3^13; expected from solution.py.

## Findings
- **should-fix S1:** Q010 says "không phân biệt hoa thường" but loops never shows case-insensitive matching and `.lower()` arrives next lesson. Add a one-line pattern in b01/b02 (e.g. `ch in "aeiouAEIOU"`), else An may stall on 'Interview'. The generated check-q010 hints are generic placeholders (tool-owned).
- **nit N1:** `while ... else` is not mentioned; b07 only shows `for ... else`. One sentence would close it.
- **nit N2:** b09 (collatz) loops forever for n <= 0; say "n dương" in the statement.

## Learner-sim
An (VN, no Python): **4/5**. Strong progression (accumulator, range pitfalls, for-else); Q010 case handling is the only gap.
