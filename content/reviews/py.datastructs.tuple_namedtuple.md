# Review: py.datastructs.tuple_namedtuple (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 1 should-fix)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 80 problems"; `ruff check .` clean. 16 blocks, `est_minutes: 12`; graded: b03, b06, b09, b13, b14 (code_exercise), b15 (problem_ref).

## Prereq discipline (key)
- `mastery_check: l1 [Q020], l2 [X006], l3 []`. The gate is curated: content_loader narrows items to the lesson's `mastery_check` per level, so Q021 (concept) is NOT served as the write_code gate.
- Q020 (read_code, swap `x, y = y, x`, p unchanged) is taught by b04/b05. OK.
- X006 `best_scorer` (checks_extra, merged into `content/checks`, `problem_id: check-x006`): reference is a single `for name, score in records` loop with `>` and a tuple return. No `lambda`, `sorted(key=)`, `max(key=)` or classes. The statement hints the unpacking loop. Genuine level-2 write_code, loop + tuple only. Hidden tests (9): single, ties (first wins), all equal, negatives, first/last max, extremes, random n=1000; expected from solution.py. Correct.
- `class X(NamedTuple)` is only a one-clause awareness mention (b10). OK.

## Correctness (checked by hand)
- b02 `3 4 2 (3, 4, 5) (3,)`; types int/tuple/tuple. b05 `2 1 10 [20, 30, 40] 50`. b06 `1 [2, 3, 99] 4 (2, 3)`. b08 `True False b` / `2`. b11 `3 4 Diem(x=3, y=4) 7` / `Diem(x=10, y=4) Diem(x=3, y=4)`. All correct.
- Hashability claim (hashable iff all elements hashable; `(1, [2])` unhashable), `(x,)`, `*rest` gives a list, swap RHS evaluated first: correct. Quiz distractors fair (b03, b09).
- b13 accepts `b, a`, `b,a`, `(b, a)`. b14 solution right; starter is a `def` skeleton (same pattern as the dict model).

## Problem: flipping-an-image (LC832)
Bilingual, `rewrite_required: true`, published. io list[list[int]], exact compare, deterministic. Hidden: n=1, all ones, all zeros, random up to n=20. Wrong: `flip_only` (fails all-ones/all-zeros), `invert_only` (fails asymmetric rows); each fails a hidden test (green validator confirms). brute.py is independent. Solution uses only `for`, slicing `[::-1]`, `append`.

## Findings
- **should-fix S1 (b01):** says `p.append(1)` "báo TypeError". It is `AttributeError: 'tuple' object has no attribute 'append'`; only item assignment `p[0] = 9` is TypeError. Reword.
- **nit N1:** LC832 is a nested-list/loop problem; it uses no tuple or unpacking, so the practice problem does not reinforce the lesson (plan-assigned, acceptable).
- **nit N2:** unpacking mismatch -> `ValueError` is stated but never shown; `tuple(list)`, `.count`, `.index` not mentioned. Fine to omit.
- **nit N3:** X006 example shows output `["Binh", 9]` (list syntax) while the text says return a tuple; the harness normalizes so a tuple passes. One clause in the statement would avoid confusion.

## Length
16 blocks for 12 min equals the dict model; blocks are short and alternate text/code/quiz, one concept each. Acceptable, not bloated.

## Learner-sim
An (VN, knows list/dict): **4/5**. Good flow (immutability, unpacking, hashable keys, namedtuple). Loses a point for the AttributeError slip and a practice problem that does not exercise tuples.
