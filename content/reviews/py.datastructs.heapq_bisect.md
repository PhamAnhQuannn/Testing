# Review: py.datastructs.heapq_bisect (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; one minor should-fix on the Q032 gate statement, tool-owned)

Run: `validate_content.py --pyodide` -> "content OK: 40 lessons, 84 problems"; `ruff check .` clean. 15 blocks, 14 min; graded: b05, b08, b11, b12, b13 (two code_exercises), b14 (problem_ref).

## Prereq discipline
- `mastery_check: l1 [Q031], l2 [Q032]`. Q031 (read_code: heapify/heappush/heappop, nsmallest, bisect_left/right) is fully taught in b01-b10.
- Q032 `kth_largest(nums, k)`: reference = the lesson's own b06/b07 size-k pattern (`heappush`, pop if `len > k`, return `h[0]`). Uses only heapq, a `for` loop and `len`; no lambda/`key=`/classes. I traced the reference through all 7 stored tests (sample `[3,2,1,5,6,4],2 -> 5`; dups `[7,7,7],2 -> 7`; `k=n`; negatives): all consistent, and `nlargest(k,nums)[-1]` passes too. Solvable with taught-only concepts: CONFIRMED.
- `key=` appears only as a one-line awareness note (b09, "chỉ nhận biết"); exercises use plain number lists. Compliant.

## Correctness (checked by hand)
b02 `0 0 1 2`; b04 `9` and `(1, 'an sang') (2, 'ngu')` (tie on priority 2 broken by the string, "ngu" < "viet bai"); b07 `[9, 8] [1, 2]` / `5 [5, 8, 9]`; b08 `4`; b10 `1 3 3` / `[1,3,3,4,5]` / `5 0`; b11 answer b (4-1=3). Claims right: min-heap only, no maxheap, negate trick, heap is not sorted beyond `h[0]`, heappush/heappop O(log n), heapify O(n), nlargest/nsmallest return sorted lists, size-k pattern O(n log k), `bisect_right - bisect_left` = count, `insort` O(n), `key=` since 3.10. b12/b13 solutions and tests correct (`[]` target 3 -> 0).

## Problem: running-kth-largest (original, no rewrite_required)
Deterministic `list[int]` with `-1` before k numbers; exact compare. Bilingual, examples worked out correctly ([4,5,8,2],3 -> [-1,-1,4,4]). Hidden 10: single, k>n (never full), duplicates, increasing/decreasing, extremes, random, stress n=2e4 with k=1000 and k=n. `brute.py` (sort every prefix) + `small_inputs` (dups, k up to 14 > n) present, cross-check green. `wrong/early_report` (reports at k-1) and `wrong/kth_smallest` fail hidden; `slow/sort_every_prefix` is O(n^2 log n) and is the TLE one (500ms, n=2e4). Constraints are consistent with the tests.

## Findings
- **should-fix S1 (tool-owned, low):** check-q032's statement is only "Viết `kth_largest(nums, k)` dùng heapq (min-heap kích thước k), O(n log k)": no constraints (k <= len), no statement that duplicates count separately (tests assume it; h02 `[7,7,7],2 -> 7`), EN statement is a placeholder, and the 3 hints are generic. A beginner can still solve it from the lesson, but the "k-th largest with duplicates" definition is implicit. Fix in the source assessment/convert_checks (not a content hand-edit). Not blocking.
- **nit N1:** "heap kích thước k" and O(n log k) cannot be enforced by 6 tiny hidden tests (a `sorted(...)[-k]` passes); fine for a gate.
- **nit N2:** `nlargest` is taught as a separate exercise (b12) from the manual size-k pattern the gate wants; the manual pattern is only seen in b07/b08 + the practice problem. Reasonable, but a manual-heap code_exercise would align the gate better.

## Length
15 blocks / 14 min; heapq then bisect with check after each. Not bloated.

## Learner-sim
An: **4/5**. Explanations and traps (heap not sorted, tuple tie-break, left vs right) are clear; I lose one point because the gate prompt is terse and the size-k pattern gets only a predict + the practice problem before the gate.
