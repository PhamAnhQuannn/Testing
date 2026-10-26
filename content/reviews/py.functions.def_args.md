# Review: py.functions.def_args (reviewer pass, independent)

**Verdict: APPROVE** (no blockers, no should-fixes; 2 nits)

Run: `validate_content.py --pyodide` -> "content OK: 40 lessons, 89 problems"; `ruff check .` clean; `pytest tools/tests -q` -> 135 passed (after final gen_hidden). 16 blocks, 15 min; graded: b03, b06, b09, b11, b12, b13, b14, b15.

## Prereq discipline
- Gate `l1 [Q033]` (read_code, `def f(x, acc=[])`, `f(1), f(2)` -> `[1, 2] [1, 2]`): taught exactly in b04/b05/b06. `l2 [Q034]` fib: loop + two variables + `def`/`return`; solvable with taught-only concepts (py.core.loops, tuple swap `a, b = b, a + b`). The practice problem hints give the same pattern. CONFIRMED.
- Lesson uses only core + list/tuple/dict ideas; `*args`/`**kwargs`, defaults, pass-by-reference are taught before use. No classes/decorators/closures. Compliant.

## Correctness
Executed every code_sample/predict: b02, b05, b06 (`1 2 1 3`), b08, b11 (`[0, 6] [1, 5] 5`) all match expected_output. Claims checked: default evaluated once at `def` time, fix with `None` sentinel (b04, b05 `tag_ok`); `return a, b` is a tuple; positional-before-keyword; params after `*args` are keyword-only; `*args` -> tuple, `**kwargs` -> dict; def parameter order; no-return -> `None`; annotations not enforced; pass-by-object-reference with in-place vs rebind distinction. b09 explanation (`sum(([1,2,3],))` TypeError, `**` needs a mapping) right. b12/b13 solutions pass all their tests.

## Problems
- `create-target-array-in-the-given-order` (LC1389, rewrite_required true): EN + VI statements re-worded, constraints/examples correct. Solution uses `list.insert` (taught in py.datastructs.list). gen.py seeded; gen == hidden.jsonl verified; expected == solution verified. wrong/insert_after fails 7/10, overwrite_slot 8/10.
- `fibonacci-number` (LC509, rewrite_required true): deterministic `fib(n)`, n<=30. wrong/off_by_one fails 9/10, wrong/base_case fails exactly the n=0 case (1/10): well targeted. brute.py + small_inputs 0..15 present.
- `check-q034`: original check, 11 hidden up to n=90, gen == hidden, expected from solution. No wrong/ dir (convention for checks).

## Findings
- **nit N1:** b10 explains docstring/annotation in prose only; no tiny code example (`"""..."""`, `-> int`). Optional.
- **nit N2:** the gate says "vòng lặp" and recursion is never discussed; intentional and fine.

## Length
16 blocks / 15 min: dense but each block is short; defaults trap, args, ref-semantics each get text -> sample -> check. Not bloated.

## Learner-sim
An: **4.5/5.** The mutable-default section is very clear (the predict with a mixed call is excellent); the pass-by-reference predict b11 is a fair hard item. Half a point off for no docstring code example.
