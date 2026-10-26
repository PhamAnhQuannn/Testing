# Review: py.functions.lambda_hof (reviewer pass, independent)

**Verdict: APPROVE** (no blockers, no should-fixes; 3 nits)

Run: validate "content OK: 40 lessons, 89 problems"; ruff clean; pytest 135 passed. 13 blocks, 14 min; graded: b03, b06, b09, b10, b11, b12.

## Prereq discipline
- `l1 [Q035]`: `sorted(..., key=lambda s: -len(s))`, `map(lambda ...)`, `filter(None, ...)`. VERIFIED taught before the gate: b04 explains `map`, `filter`, `filter(None, ds)` and introduces `key=` with the identical `sorted(ds, key=lambda w: -len(w))` example; b05 runs it (`['ccc', 'bb', 'a']`). `sorted()` itself was taught in py.datastructs.list. Q035 does NOT depend on sorting_keys. CONFIRMED.
- `l2 [X008]`: `run_pipeline(x, ops)`: dict of name -> lambda, then a loop. Only lambdas (b01/b02), dict-of-functions (b02 `ops` dict is exactly this), for loop. Taught-only. It is the write_code gate; Q036 (`concept`, lambda vs def) stays in the pool as a concept item, not the l2 gate. checks_extra X008 is merged into generated `content/checks/py.functions.lambda_hof.yaml` (contains Q035, Q036, X008). CONFIRMED.
- Practice `height-checker` uses `sorted` and `zip` (both taught earlier). Closures: awareness only (b07 "sẽ giải thích ở bài scope sau"); b08 `make_adder` is a short demo, nothing relies on it. Compliant.

## Correctness
Executed b02, b05, b06, b08: all match. Checked: lambda body is one expression, no `return`/assignment; ternary allowed; `map`/`filter` return one-shot iterators (b05 `print(list(m), list(m))` -> second is `[]`; b09 quiz); `filter(None, ds)` keeps truthy; multi-iterable `map`; `reduce` with initial value and empty input; `partial(power, exp=2)` and positional `partial(power, 2)(10)=1024`; `operator.mul/neg/itemgetter`; comprehension preferred over nested lambdas. b10/b11 solutions pass all tests.

## Problems
- `height-checker` (LC1051, rewrite_required true): re-worded statements, constraints/examples right (`[1,1,4,2,1,3] -> 3`). gen == hidden, expected == solution; brute + small_inputs present. wrong/sort_in_place (the aliasing trap from the lesson) fails 7/10, wrong/descending fails 7/10.
- `check-x008`: genuine L2 write_code, deterministic, correct. 8 hidden (empty ops, order matters, negative square, extremes), gen == hidden, expected from solution. Hints go idea -> code. An if/elif solution also passes; fine for a gate.

## Findings
- **nit N1:** height-checker solution.py uses `zip(..., strict=True)` (3.10+, ruff B905) which the lesson never mentions; learners read solutions. Harmless on Pyodide.
- **nit N2:** `key=` is explained before sorting_keys in one paragraph (plan's explicit design); the forward pointer is clear.
- **nit N3:** the only practice problem exercises `sorted`/`zip`, not `map`/`filter`/`reduce`; exercises b10/b11 cover those. `partial` has no exercise.

## Length
13 blocks / 14 min; b07/b08 pack reduce + partial + operator + returning a function. Slightly dense, not bloated.

## Learner-sim
An: **4/5.** The one-shot iterator trap is shown, not just stated; the lambda-validity quiz is good. b07 packs four ideas so partial/operator feel fast.
