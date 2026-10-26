# Review: py.core.getting_started (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 3 should-fix, one needs a Quan pedagogical decision)

Run: `validate_content.py --pyodide` -> "content OK: 40 lessons, 68 problems"; `ruff check` clean; `ruff format --check` 242 files formatted. 11 blocks, 3 graded (b03, b05, b08) + b09 code_exercise. All expected outputs re-verified by running (sqrt 4.0; ceil/floor 3 2; circle_area 3.14/12.57/0.0/314.16; b05 B C D).

## Findings
- **should-fix / Quan decision - b09 previews `def`/`return`.** Functions are not in cs.onramp-only prereqs. The in-text parenthetical (b09) explains def/indent/return in one sentence and the starter is given, so it is survivable, but `pass`, parameter `r`, and "calling" are never explained, and it is the first coding exercise. Options: (a) keep, add 1-2 lines ("hàm = đoạn code đặt tên, nhận đầu vào r, trả kết quả; sẽ học kỹ ở bài sau"); (b) make b09 function-free (e.g. print area of fixed r with math.pi, round) and leave functions to the problem. Caveat: the problem (add-two-integers) and check X001 are function-mode, so the learner meets `def` there anyway; (a) is the pragmatic choice. Reviewer recommends (a).
- **should-fix - Q002 (check, l2) uses `for`, `range`, `+=`**, none taught in this lesson; a day-1 learner who only has this lesson cannot hand-trace it. Either confirm cs.onramp covers loops, or swap Q002 to an if/else/indent trace (as b05). Note the lesson's own teaching target is indentation, so it fits conceptually.
- **should-fix - b05 / b04 use `x = 2`, `if x > 3`, `else` without any intro** (variables, comparison, if/else). Add one sentence in b04 or an intro line before b05 unless onramp is confirmed to cover them.
- **nit - b01** `python -m http.server` aside is noise for a beginner; drop or move out.
- **nit - add-two-integers starter** has type hints (`num1: int`, `-> int`) and `pass` unexplained; acceptable (project convention) but hint 1/2 could mention "def ... -> int là chữ ký hàm".
- **nit - b04** "79-100 ký tự" is vague (PEP 8 = 79; ruff repo limit 100); say "khoảng 79".
- **nit - b07/b08** traceback fine and accurate (last line = error type, `line N` above); b08 distractors fair (b and c are plainly wrong), but option b is weak - fine for an easy item.
- **nit - b02** `Tổng: 5` relies on `print` with comma adding a space; not explained, harmless.

## Problem add-two-integers (OK)
- Bilingual statement, constraints, 3 examples consistent with sample.jsonl; `source.rewrite_required: true` present; solution is `return num1 + num2`.
- hidden.jsonl matches gen.py inputs; expected values all arithmetically correct (consistent with generated-from-solution).
- wrong/subtract.py fails s1 onward; wrong/ignore_sign.py passes s1 but fails s2 and hidden (negatives): both genuinely fail. Hidden coverage (12 cases incl. bounds, zeros, negatives) is adequate for a trivial problem; `abs`/`-`/`*` mutants all caught.

## Check X001 (OK)
- Real level-2 write_code: `math.ceil(items/per_page)` ties directly to b06 (`ceil`) and b09 (`import math`). Hidden covers 0 items, exact multiple (20,10), off-by-one (21,10), per_page=1, 1e6/7=142858 (float division safe at this range). Expected values correct. Merged correctly into content/checks (X001 present with problem_id, rubric); lesson `mastery_check.l2: [Q002, X001]` references it. Problem status `validated` vs lesson `published` is consistent with the pipeline.
- Nit: X001 uses `/` true division; not explicitly taught, but hint 1 shows `25 / 10 = 2.5`, which suffices.

## Summary/body consistency
Summary bullets match the body (REPL/script, indentation, comment/docstring/snake_case, math, traceback). Note snake_case/docstring are mentioned in b04 only briefly; fine.

## Learner-sim impression
An (VN, no Python): **ease-of-understanding 4/5** - friendly, short, good order, traceback block is the highlight; loses a point on unexplained `def`/`pass`/`x = 2`/`if` and the `for` in Q002.
