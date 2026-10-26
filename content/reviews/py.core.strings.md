# Review: py.core.strings (reviewer pass, independent)

**Verdict: APPROVE-WITH-NITS** (no blockers; 1 should-fix)

Run (WSL): `validate_content.py --pyodide` -> "content OK: 40 lessons, 76 problems"; `ruff check .` clean. 11 blocks; graded: b02, b05, b07, b08 (quiz_fill), b09 (code_exercise).

## Prereq discipline (key)
- `mastery_check: l1 [Q011], l2 [Q012], l3 [Q013]`. W185 (`reverse_words`, uses `split()[::-1]`, list-based) is in the generated pool but not curated, so l2 serves Q012 only (curated filter, `content_loader.py:242`).
- Q011 read_code: slicing, `[::-1]`, `count`, `upper`; output `ter wei 2 INTERVIEW` is correct.
- Q012 (`is_pal`): solvable with strings only: loop, `c.isalnum()`, `c.lower()`, build `t = t + ...`, compare `t == t[::-1]`. The reference uses a list but nothing requires it.
- Q013 (`compress`, d3): solvable with `while`/`for` + index or previous-char tracking, conditionals, `str(count)`, string concatenation. No list needed (the reference's `out=[]`/join is optional). Appropriate reach for d3.
- length-of-last-word is practice only (b10); uses `rstrip`/`rfind`/`len` taught here; not a gate.
- Previews: `split()` returning a list is stated once and labeled "học ở py.datastructs": acceptable, but see S1. The b09 exercise just iterates `for word in full_name.split()`, which needs only "for over an iterable".

## Correctness (verified by hand)
- b02 outputs `i w ter iew` / `itriw weiv 9`. b04: stripped length 16; find("o")=7, rfind=14, count=2; split outputs, join `2026-10-25`, isalnum/isdigit/isalpha lines all correct. b07: `007 | 1,234,567 | 25.6% |    Lan|Lan   |` correct. b05 (b) correct; b08 `-3` correct. "café" = 5 bytes in UTF-8 correct. Slicing never raises IndexError; `s[0]="I"` -> TypeError: correct. b09 tests (extra spaces) correct.
- length-of-last-word: bilingual, rewrite_required true; wrong/first_word, no_rstrip, off_by_one each fail hidden (green validator confirms); hidden covers single char, leading/trailing spaces, 10^4 max; expected from solution.py.

## Findings
- **should-fix S1:** b03/b04 use list syntax (`["2026","10","25"]`, printed `['a','b','','c']`) and an undefined `ds`. Add one sentence: `[...]` is a list (a sequence in square brackets, covered in py.datastructs); here only "join takes a sequence of strings".
- **nit N1:** b01 and the summary say "mọi phương thức của `str` đều trả về chuỗi mới"; `find/count/startswith/isdigit` return int/bool (b03 says "chuỗi/giá trị mới"). Reword to "không sửa chuỗi gốc".
- **nit N2:** Q012/Q013 generated hints are generic placeholders; a beginner gets no real nudge (tool-owned).
- **nit N3:** format-spec and bytes content is dense for 12 min; acceptable as "chỉ cần biết sơ".

## Learner-sim
An (VN, no Python): **4/5**. Slicing and immutability land well; the list syntax in b04 is the one unexplained jump.
