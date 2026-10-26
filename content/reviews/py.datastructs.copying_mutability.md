# Review: py.datastructs.copying_mutability (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers, no should-fix)

Run: `validate_content.py --pyodide` -> "content OK: 40 lessons, 84 problems"; `ruff check .` clean. 16 blocks, 14 min; graded: b05, b10, b12 (predict), b13 (code_exercise), b14/b15 (problem_ref).

## Prereq discipline
- `mastery_check: l1 [Q029], l2 [X007]`. Q029 (read_code, `[[0]*2]*2` vs comprehension) is taught in b08-b10. Q030 (concept) exists in checks but is NOT in the lesson gate, so it is never served as the write_code gate. Good.
- X007 `plus_one_copy`: solution is nested `for` + `append` (check-x007/solution.py), return `[new_grid, grid]`. Uses only list/loops/copy ideas from the lesson. No lambda/class/generator. `copy.deepcopy` alternative (hint 3) is taught in b06. Solvable with taught-only concepts: CONFIRMED.
- Genuine level-2 write_code (difficulty 2, 5 min, problem_id check-x007), rubric = pass all hidden. Merged into generated `content/checks/...yaml`; curated via lesson `mastery_check`. Hidden (8) include empty grid, empty row, ragged rows, negatives, 20-row random. A student who mutates `grid` in place or returns `[grid, grid]` fails (the second element is compared), and `grid[:]`+in-place edit fails: the test really exercises aliasing.
- Lesson stays taught-only: `import copy` / `deepcopy` / `is`/`id` are in-lesson; `key=`/lambda absent; rotate uses slicing + `%=` (taught).

## Correctness (checked by hand)
b02 `[1, 2, 3, 4] True True` / `5 6`; b04 `[[1,2,9],[3]]`, `[[1,2,9],[3],[7]]`, `False True`; b05 answer b (shallow, `b[1]=[9]` rebinding only the outer) correct; b07 deepcopy incl. self-referencing `d[1] is d` True; b09 `[[1,0,0],[1,0,0]] True` / `[[1,0,0],[0,0,0]] False`; b10 `[[0, 7], [0, 7]] True`; b12 `[1, 2, 3] (1, 2)`. Claims right: `b = a` is aliasing; mutable/immutable lists; shallow-copy forms; `a += [3]` in place vs `a = a + [3]` new; tuple `+=` rebinds; list inside tuple still mutable. No inaccuracy found.

## Problems
- **pascals-triangle (LC118, easy, rewrite_required)**: bilingual, deterministic `list[list[int]]`, exact compare; hidden 11 (1..30). Wrong `all_ones`, `shared_row` each fail a hidden test (validator green). No brute/slow (acceptable: easy, n<=30, expected from solution.py). The aliasing hint ties to the lesson well.
- **rotate-array (LC189, MEDIUM, rewrite_required)**: `brute.py` present (independent step-by-step pop/insert), `small_inputs` present (1..12 elems, k 0..40, often k>n); cross-check passes (green validator). Returns a NEW rotated list, exact compare: deterministic (no in-place semantic ambiguity). Hidden 10 incl. k=0, k=n, k>n, n=1, stress n=5e4 k=99999 (341KB, under cap). `wrong/no_mod` (negative-slice, fails k>n and k=0 / k=n) and `wrong/rotate_left` fail hidden; `slow/one_step_at_a_time` O(n*k) TLE at 300ms (5e4 x ~5e4). Narrowed constraints (n<=5e4, values -100..100, k<=1e5): ACCEPTABLE. They only exist because of the 1MB hidden cap; they still separate O(n) from O(n*k). Statement honestly says "return a new list". Note the original LC189 is in-place `None`; this is a rewrite, flagged below.

## Findings
- **nit N1:** the LC189 "medium" is mostly a slicing one-liner after `k %= n`; fine for a beginner medium, but the in-place O(1)-space variant (the real interview question) is not asked. Optional extra later.
- **nit N2:** b06 packs the deepcopy-vs-cycles remark (awareness) into a text block; dense but marked as "nhận biết".
- **Quan item Q1:** the LC189 rewrite (in-place -> returns new list; narrowed constraints) and the 1MB-cap rationale should be confirmed by Quan as an accepted `rewrite_required` outcome.

## Length
16 blocks / 14 min. Each concept: short text + sample + check. Not bloated.

## Learner-sim
An: **5/5**. Clear label metaphor -> `is`/`id` -> shallow vs deep -> the 2D trap -> `+=`. Predict items test the exact misconceptions; the gate (X007) directly tests the lesson's idea.
