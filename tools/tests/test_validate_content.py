import shutil

from common import dump_yaml, load_json, load_yaml
from validate_content import Validator, find_cycle

PROBLEM = "problems/py.datastructs.dict/ransom-note"
DICT_LESSON = "lessons/py/py.datastructs.dict.yaml"


def problem_errors(content, *, keep_slow=False):
    if not keep_slow:  # the slow check waits for a 3 s timeout
        shutil.rmtree(content / PROBLEM / "slow")
    validator = Validator(content)
    ids = {s["id"] for s in load_json(content / "index/subtopics.json")["subtopics"]}
    validator.check_problem(content / PROBLEM, ids)
    return validator.errors


def edit(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")


def test_ransom_note_passes_every_check(content):
    assert problem_errors(content, keep_slow=True) == []


def test_schema_violation_stops_the_problem_early(content):
    edit(content / PROBLEM / "problem.yaml", "difficulty: easy", "difficulty: trivial")
    errors = problem_errors(content)
    assert len(errors) == 1 and "difficulty" in errors[0]


def test_stale_hidden_tests(content):
    edit(
        content / PROBLEM / "tests/hidden.jsonl",
        '"expected":false,"tags":["edge"]',
        '"expected":true,"tags":["edge"]',
    )
    assert any("stale" in e for e in problem_errors(content))


def test_wrong_reference_solution(content):
    edit(content / PROBLEM / "solution.py", "return True\n", "return False\n")
    assert any("solution WA" in e for e in problem_errors(content))


def test_solution_over_the_time_share(content):
    solution = content / PROBLEM / "solution.py"
    slow_on_big = "if len(magazine) > 1000:\n        time.sleep(0.35)\n    have = {}"
    solution.write_text("import time\n\n" + solution.read_text().replace("have = {}", slow_on_big))
    assert any("over 0.3 x time_ms" in e for e in problem_errors(content))


def test_brute_force_disagreement(content):
    edit(content / PROBLEM / "brute.py", "return True", "return len(ransom_note) < 3")
    assert any("disagrees with brute.py" in e for e in problem_errors(content))


def test_brute_force_is_required_for_medium(content):
    edit(content / PROBLEM / "problem.yaml", "difficulty: easy", "difficulty: medium")
    (content / PROBLEM / "brute.py").unlink()
    assert any("brute.py is required" in e for e in problem_errors(content))


def test_wrong_solution_that_passes(content):
    shutil.copy(content / PROBLEM / "solution.py", content / PROBLEM / "wrong/actually_right.py")
    assert any("actually_right.py passes every hidden test" in e for e in problem_errors(content))


def test_slow_solution_that_is_fast_enough(content):
    shutil.copy(content / PROBLEM / "solution.py", content / PROBLEM / "slow/fast.py")
    assert any("fast.py must exceed" in e for e in problem_errors(content, keep_slow=True))


def test_starter_that_solves_the_problem(content):
    solution = (content / PROBLEM / "solution.py").read_text()
    path = content / PROBLEM / "problem.yaml"
    problem = load_yaml(path)
    problem["starter"]["python"] = solution
    path.write_text(dump_yaml(problem), encoding="utf-8")
    assert any("starter code already passes" in e for e in problem_errors(content))


def test_too_few_hidden_tests(content):
    hidden = content / PROBLEM / "tests/hidden.jsonl"
    hidden.write_text("".join(hidden.read_text().splitlines(keepends=True)[:5]))
    assert any("hidden has 5 tests" in e for e in problem_errors(content))


def lesson_errors(content):
    validator = Validator(content)
    validator.check_lessons(validator.check_index(), {"ransom-note"})
    return validator.errors


def test_lesson_code_sample_output_is_checked(content):
    edit(content / DICT_LESSON, 'expected_output: "0911 True không có"', 'expected_output: "nope"')
    assert any("block b02" in e and "nope" in e for e in lesson_errors(content))


def test_lesson_code_exercise_solution_is_checked(content):
    edit(content / DICT_LESSON, "return sorted(set(nums))", "return nums")
    assert any("block b09: solution" in e for e in lesson_errors(content))


def test_lesson_problem_must_exist(content):
    edit(content / DICT_LESSON, "problem_id: ransom-note", "problem_id: nope")
    assert any("unknown problem nope" in e for e in lesson_errors(content))


def test_lesson_block_ids_must_be_unique(content):
    edit(content / DICT_LESSON, "id: b02", "id: b01")
    assert any("duplicate block ids" in e for e in lesson_errors(content))


def test_published_lesson_needs_graded_blocks(content):
    path = content / DICT_LESSON
    edit(path, "status: draft", "status: published")
    edit(path, "min_items: 3", "min_items: 4")
    assert any("at least 4 graded" in e for e in lesson_errors(content))


def test_non_draft_lesson_cannot_be_empty(content):
    edit(content / "lessons/py/py.core.loops.yaml", "status: draft", "status: validated")
    assert any("blocks" in e for e in lesson_errors(content))


def test_every_subtopic_needs_a_lesson(content):
    (content / "lessons/py/py.core.loops.yaml").unlink()
    assert any("missing lessons: ['py.core.loops']" in e for e in lesson_errors(content))


def test_prerequisite_cycle(content):
    assert find_cycle({"a": {"b"}, "b": {"c"}, "c": {"a"}}) == ["a", "b", "c", "a"]
    assert find_cycle({"a": {"b"}, "b": set()}) is None


def test_solution_that_does_not_compile_is_reported_without_crashing(content):
    (content / PROBLEM / "solution.py").write_text("def can_construct(:\n")
    errors = problem_errors(content)
    assert any("solution CE" in e for e in errors)


def test_wrong_solution_must_fail_a_hidden_test_not_just_a_sample(content):
    only_sample = (content / PROBLEM / "solution.py").read_text() + (
        "\n_correct = can_construct\n\n\n"
        "def can_construct(a, b):\n"
        "    return True if (a, b) == ('aa', 'ab') else _correct(a, b)\n"
    )
    (content / PROBLEM / "wrong/sample_only.py").write_text(only_sample)
    assert any("sample_only.py passes every hidden test" in e for e in problem_errors(content))


def test_first_example_must_be_sample_one(content):
    edit(
        content / PROBLEM / "problem.yaml",
        'ransom_note = "a", magazine = "b"',
        'ransom_note = "z", magazine = "b"',
    )
    assert any("examples[0] must be sample test 1" in e for e in problem_errors(content))


def test_unknown_param_type_is_a_schema_error(content):
    edit(
        content / PROBLEM / "problem.yaml",
        "type: str}, {name: magazine",
        "type: strng}, {name: magazine",
    )
    assert any("params" in e for e in problem_errors(content))
