# Review: py.datastructs.collections_module (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 1 should-fix)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 80 problems"; `ruff check .` clean. 16 blocks, `est_minutes: 13`; graded: b05, b08, b11, b13, b14 (code_exercise), b15 (problem_ref).

## Prereq discipline (key): Q028 gate VERIFIED passable without lambda/key=
- `mastery_check: l1 [Q027], l2 [Q028], l3 []`. Q027 (read_code: Counter/defaultdict/deque) is taught.
- Q028 `top_words(words, k)`: the vi statement is "k từ xuất hiện nhiều nhất; hoà thì từ nhỏ hơn theo thứ tự chữ cái đứng trước". It does NOT require lambda or `key=`; only the author's reference solution uses `sorted(c, key=lambda ...)`.
- I ran `[w for w, _ in Counter(sorted(words)).most_common(k)]` against check-q028's sample and all 6 hidden tests: **7/7 match expected, 0 failures**. Ties are genuinely exercised: h01 `["b","a"], k=1 -> ["a"]` (fails without the pre-sort), h03 (x,y), h04 (a,b,c all tied). CPython documents that equal counts keep first-encountered order and `most_common(k)` is stable, so the claim in b03 is correct.
- The route is taught in b03 (text) and b04 (runnable sample `Counter(sorted(tu)).most_common(2)`); `sorted` is taught in the list/dict lessons. No heapq/bisect, classes or generators needed.

## Correctness (checked by hand)
- b02 `Counter({'a': 3, 'n': 2, 'b': 1}) 3 0` / `[('a', 3), ('n', 2)]`; b04 `Counter({'a': 3, 'b': 2, 'c': 1}) Counter({'a': 1}) 0` / `[('a', 2), ('b', 2)]`; b05 answer b; b07 incl. `False 0 True` (print args evaluate left to right); b08 `2 [] 3` (explanation right); b10 `0 4 [1, 2, 3]` / `[3, 1, 2]` / `[3, 4, 5]`; b11 answer b. All correct. Q027 expected `[('a', 3)] {'x': [1]} [0, 1, 2]` correct.
- Claims: Counter missing key gives 0 without inserting; `a - b` drops non-positive; defaultdict read inserts; deque O(1) at both ends, `maxlen`, `rotate`; list `pop(0)`/`insert(0, x)` O(n); OrderedDict awareness only. All correct. b06 refers to `get`/`setdefault` of the dict lesson; `.get` is taught there (setdefault only lightly), acceptable.

## Problem: majority-element (LC169)
Bilingual, `rewrite_required: true`, published. int, exact, deterministic. `_with_majority` guarantees count n//2+1 in every hidden and small input (incl. n=50000 and 49999), so a real majority always exists. Hidden (11): single, all equal, negatives, close margin, 1e9, stress. Wrong: `largest_value` (`max`) and `least_common` (`most_common()[-1]`) each fail hidden tests (green validator confirms; least_common passes only trivial single/all-equal inputs). brute.py (`nums.count`) is independent. Expected from solution.py.

## Findings
- **should-fix S1:** the one skill the level-2 gate hinges on (pre-sorting for the alphabetical tie-break) is never practiced in a graded block; it appears only in b03 text and the b04 sample. Add one quick graded item before the gate (e.g. predict_output of `Counter(sorted(["b","a","b","a"])).most_common(1)` -> `[('a', 2)]`) or point the b14 hint at b03. Otherwise An will likely reach for `key=lambda` (untaught) and stall.
- **nit N1:** densest of the three lessons (Counter + arithmetic + tie rule, defaultdict, deque, OrderedDict); 13 min is optimistic. Not bloated enough to cut.
- **nit N2:** check-q028 hints are generic tool-generated placeholders and do not mention the sort trick (tool-owned).
- **nit N3:** b11 "O(n^2)" for 100000 pops is right in complexity terms even though memmove is fast in practice; fine for the lesson.

## Length
16 blocks (equals the dict model). Acceptable given three tools, each with text/sample/check.

## Learner-sim
An: **4/5**. Well sequenced; the defaultdict "read creates the key" trap is a good catch. The gate is passable, but the tie-break trick needs one practice rep before it counts.
