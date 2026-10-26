# Review: py.functions.sorting_keys (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 1 minor should-fix: b04 wording)

Run: validate "content OK: 40 lessons, 89 problems"; ruff clean; pytest 135 passed. 15 blocks, 14 min; graded: b03, b08, b09, b12, b13, b14.

## Prereq discipline
- `l1 [Q037]`: `sorted(data, key=lambda t: (-t[1], t[0]))`: same key shape taught in b06/b07. `l2 [Q038]` `sort_words`: `sorted(words, key=lambda w: (len(w), w))`: taught in b06 ("ngắn trước, hoà thì theo chữ cái"). Taught-only. CONFIRMED.
- `itemgetter`, `attrgetter`, `cmp_to_key` are labelled awareness ("chưa cần dùng"); only `itemgetter` has a tiny demo. No classes used. Compliant.

## Correctness
Executed b02, b05, b07, b08, b11: all match. Checked: `sorted` takes any iterable and returns a new list; `.sort()` list-only, in place, returns `None` (b03); `a = a.sort()` trap; uppercase before lowercase; `key` called once per element; stability including with `reverse=True` (b08: `y` before `w` is right); tuple key + negation; strings cannot be negated (b09 option c is a real TypeError); `sorted(dict)` gives keys; dict by value; Timsort O(n log n), near O(n) on nearly sorted data. b12/b13 solutions pass their tests.

## Problems
- `rank-students` (source: original, correctly no rewrite_required): bilingual; constraints (distinct lowercase names) make the tie-break well defined; examples correct. **Determinism confirmed**: `_records` sorts the name set before the seeded shuffle (set-order bug fixed); I re-imported gen.py in a fresh process and `hidden_inputs()` args equal hidden.jsonl for all 10 cases; expected == solution for all. Covers empty, single, ties, all-tied, prefix names, n=1000. wrong/score_only fails 6/10; wrong/name_desc_tiebreak fails 8/10. brute + small_inputs present.
- `check-q038`: 5 hidden (empty, single, mixed lengths, duplicates), gen == hidden, expected from solution; length-only or alphabetical-only sorts are rejected by h03/h04. Terse statement but the sample clarifies. No wrong/ dir (convention for checks).

## Findings
- **should-fix S1 (minor):** b04 last sentence: "`sort` và `sorted` đều nhận `key` và `reverse` (cũng như `max`, `min`)". Read naturally it implies `max`/`min` also take `reverse`; they take `key` but NOT `reverse`. Reword, e.g. "(`max`/`min` cũng nhận `key`, nhưng không có `reverse`)". Not blocking.
- **nit N1:** b06 mentions "hai lượt sort nhờ tính ổn định" for string-descending but never shows it. Awareness only.

## Length
15 blocks / 14 min; clean progression sort -> key -> stability/multi-key -> dict. Not bloated.

## Learner-sim
An: **4.5/5.** Very clear; the stability-with-reverse predict is the right hard item and the tuple/negation quiz exposes the string trap. Only the max/min wording could mislead.
