# Review: py.datastructs.comprehensions (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers, no should-fix)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 80 problems"; `ruff check .` clean. 15 blocks, `est_minutes: 12`; graded: b03, b05, b10, b13 (code_exercise), b14 (problem_ref).

## Prereq discipline (key)
- `mastery_check: l1 [Q025], l2 [Q026], l3 []`. Q025 (read_code: filtered square list + set comprehension) is fully taught. Q026 `flatten(m)`: reference `[x for row in m for x in row]` is exactly the b06/b07 pattern; solvable with the taught nested comprehension (or a plain nested `for` + `append`). No lambda/key/generator needed. Hidden (6) include `[]`, `[[],[]]`, empty rows. The statement says "một dòng", which tests cannot enforce (fine).
- Generator expression is awareness-only (b11/b12, `sum(x * x for x in so)`); `sum` is taught in the list lesson. Nothing from functions/classes beyond the `def` skeleton.

## Correctness (checked by hand)
- b02 `True [8, 12]`; b03 answer a; b05 `[1, 0, 3, 0] [1, 3]`; b07 `[1, 2, 3, 4, 5] [[2, 4], [6], [8, 10]]`; b09 `{'an': 2, 'binh': 4, 'chi': 3} ['a', 'b', 'c']`; b12 `242 2`. All correct. b10 accepts `x * x`, `x*x`, `x ** 2`, `x**2`.
- Claims right: trailing `if` filters vs leading `a if c else b` (else mandatory); two `for` in written order; `{}` is a dict; result is a new list. b13: `-3 % 2 == 1` is true in Python (hint says so); `[-3, 0, 7] -> [9, 49]` correct.

## Problem: how-many-numbers-are-smaller-than-the-current-number (LC1365)
Bilingual, `rewrite_required: true`, published. Deterministic list[int], exact. Hidden (10): len 2, all equal, sorted, descending, duplicates, extremes, many dups, n=500; expected from solution.py. Wrong: `counts_equal` (`<=` minus 1, wrong with duplicates) and `distinct_values` (set) each fail a hidden test (green validator confirms). brute.py is an independent O(n^2) loop. Hints use only taught constructs; hint 3 gives the answer outright (acceptable as last hint).

## Findings
- **nit N1:** no graded item practices `a if c else b` besides predict b05; a tiny fill-in could help. Optional.
- **nit N2:** b11 packs the readability rule and the generator expression into one callout; the generator half is the densest sentence for a beginner, but it is awareness-only.
- **nit N3:** check-q026 hints are tool-generated generic placeholders (tool-owned).

## Length
15 blocks, 12 min. Each concept is short text + sample + quick check. Not bloated.

## Learner-sim
An: **5/5**. Clean build-up from for-loop equivalence to filter/ternary, flatten, dict/set, with an honest "when not to use" note. Gate and practice match the teaching.
