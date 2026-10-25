"""One broken fixture per SPEC 4.4 rule: each must be reported, and the good fixture must be clean.

tools/tests/fixtures/content is a tiny, valid content tree (two subtopics, one lesson with every
graded block type, a practice problem with brute/wrong/slow solutions and a stress test, a check
problem and a checks file). Each case below breaks exactly one thing in a private copy of it.
"""

import shutil
from pathlib import Path

import pytest

from common import CONTENT, dump_yaml, load_yaml
from run_problem import pyodide_available
from validate_content import Validator

FIXTURES = Path(__file__).parent / "fixtures/content"
SUB = "py.core.variables_types"
OTHER = "py.datastructs.list"
PRACTICE = f"problems/{SUB}/count-evens"
CHECK_PROBLEM = f"problems/{SUB}/triple-it"
LESSON = f"lessons/py/{SUB}.yaml"
OTHER_LESSON = f"lessons/py/{OTHER}.yaml"
CHECKS = f"checks/{SUB}.yaml"


@pytest.fixture
def fx(tmp_path):
    target = tmp_path / "content"
    shutil.copytree(FIXTURES, target, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(CONTENT / "schemas", target / "schemas")
    return target


def errors_of(root, *, pyodide=False, public=False, keep_slow=False):
    if not keep_slow:  # the slow check waits for a timeout, so only the cases about it pay for it
        for slow in root.glob("problems/*/*/slow"):
            shutil.rmtree(slow)
    validator = Validator(root, pyodide=pyodide, public=public)
    validator.run()
    return validator.errors


def edit(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {path}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def patch_yaml(path, change):
    data = load_yaml(path)
    change(data)
    path.write_text(dump_yaml(data), encoding="utf-8")


def block(lesson, block_id):
    return next(b for b in lesson["blocks"] if b["id"] == block_id)


def drop_blocks(*ids):
    return lambda lesson: lesson.update(blocks=[b for b in lesson["blocks"] if b["id"] not in ids])


# --- index ---------------------------------------------------------------------------------


def unknown_prerequisite(fx):
    edit(fx / "index/subtopics.json", '"prerequisites": []', '"prerequisites": ["nope.x"]')


def prerequisite_cycle(fx):
    edit(fx / "index/subtopics.json", '"prerequisites": []', f'"prerequisites": ["{OTHER}"]')


def lesson_not_in_index(fx):
    edit(fx / OTHER_LESSON, f"id: {OTHER}", "id: py.datastructs.nope")


def missing_lesson(fx):
    (fx / OTHER_LESSON).unlink()


# --- lessons -------------------------------------------------------------------------------


def lesson_schema(fx):
    patch_yaml(fx / LESSON, lambda lesson: lesson.update(est_minutes=99))


def duplicate_block_ids(fx):
    patch_yaml(fx / LESSON, lambda lesson: block(lesson, "f02").update(id="f01"))


def code_sample_output(fx):
    edit(fx / LESSON, "expected_output: '7'", "expected_output: '8'")


def predict_output_mismatch(fx):
    edit(fx / LESSON, "expected_output: float", "expected_output: int")


def runnable_sample_crashes(fx):
    def change(lesson):
        sample = block(lesson, "f02")
        sample["code"] = "print(undefined_name)\n"
        del sample["expected_output"]

    patch_yaml(fx / LESSON, change)


def exercise_solution_fails(fx):
    edit(fx / LESSON, "return x * 2", "return x * 3")


def exercise_starter_passes(fx):
    def change(lesson):
        exercise = block(lesson, "f06")
        exercise["starter"] = exercise["solution"]

    patch_yaml(fx / LESSON, change)


def too_few_graded_blocks(fx):
    def change(lesson):
        lesson["checkpoint"]["min_items"] = 1  # the floor of 3 applies whatever the lesson says
        drop_blocks("f04", "f05")(lesson)

    patch_yaml(fx / LESSON, change)


def min_items_above_graded(fx):
    patch_yaml(fx / LESSON, lambda lesson: lesson["checkpoint"].update(min_items=4))


def lesson_unknown_problem(fx):
    edit(fx / LESSON, "problem_id: count-evens", "problem_id: nope")


def problem_ref_not_listed(fx):
    patch_yaml(fx / LESSON, lambda lesson: lesson["problems"].update(practice=[]))


def problem_of_another_subtopic(fx):
    patch_yaml(
        fx / OTHER_LESSON, lambda lesson: lesson["problems"].update(practice=["count-evens"])
    )


def published_lesson_links_draft_problem(fx):
    edit(fx / PRACTICE / "problem.yaml", "status: published", "status: draft")


def practice_problem_not_in_lesson(fx):
    def change(lesson):
        lesson["problems"]["practice"] = []
        drop_blocks("f07")(lesson)

    patch_yaml(fx / LESSON, change)


# --- mastery checks ------------------------------------------------------------------------


def mastery_unknown_item(fx):
    patch_yaml(fx / LESSON, lambda lesson: lesson["mastery_check"].update(l1=["Q999"]))


def mastery_wrong_level(fx):
    patch_yaml(fx / LESSON, lambda lesson: lesson["mastery_check"].update(l1=["Q902"]))


def missing_level2_write_code(fx):
    patch_yaml(fx / LESSON, lambda lesson: lesson["mastery_check"].update(l2=[]))


def no_level2_write_code_in_checks(fx):
    """The lesson lists no l2 item and the checks hold none either (SPEC 3.4/4.4)."""

    def drop_l2(checks):
        checks["items"] = [i for i in checks["items"] if i["id"] != "Q902"]

    patch_yaml(fx / CHECKS, drop_l2)
    patch_yaml(fx / LESSON, lambda lesson: lesson["mastery_check"].update(l2=[]))


def check_problem_has_four_hidden_tests(fx):
    hidden = fx / CHECK_PROBLEM / "tests/hidden.jsonl"
    hidden.write_text("".join(hidden.read_text().splitlines(keepends=True)[:4]))


def extra_item_not_merged(fx):
    extra = {"id": "X001", "difficulty": 1, "type": "concept", "minutes": 2}
    extra |= {"prompt_md": "Giải thích.", "answer_md": "Đáp án."}
    (fx / "checks_extra").mkdir()
    (fx / "checks_extra" / f"{SUB}.yaml").write_text(
        dump_yaml({"subtopic_id": SUB, "items": [extra]}), encoding="utf-8"
    )


def extra_file_misnamed(fx):
    extra_item_not_merged(fx)
    (fx / "checks_extra" / f"{SUB}.yaml").rename(fx / "checks_extra" / f"{OTHER}.yaml")


def check_item_unknown_problem(fx):
    edit(fx / CHECKS, "problem_id: triple-it", "problem_id: nope")


def check_item_problem_not_a_check(fx):
    edit(fx / CHECK_PROBLEM / "problem.yaml", "kind: check", "kind: practice")


def duplicate_check_item_ids(fx):
    def change(checks):
        checks["items"][1]["id"] = checks["items"][0]["id"]

    patch_yaml(fx / CHECKS, change)


def checks_file_misnamed(fx):
    (fx / CHECKS).rename(fx / "checks" / f"{OTHER}.yaml")


# --- problems: files and tests -------------------------------------------------------------


def problem_schema(fx):
    edit(fx / PRACTICE / "problem.yaml", "difficulty: easy", "difficulty: trivial")


def problem_directory_name(fx):
    (fx / PRACTICE).rename(fx / PRACTICE.replace("count-evens", "count-odds"))


def unknown_secondary_subtopic(fx):
    edit(fx / PRACTICE / "problem.yaml", "secondary_subtopics: []", "secondary_subtopics: [nope.x]")


def missing_hidden_file(fx):
    (fx / PRACTICE / "tests/hidden.jsonl").unlink()


def stale_hidden(fx):
    edit(
        fx / PRACTICE / "tests/hidden.jsonl",
        '"expected":0,"tags":["edge"]',
        '"expected":9,"tags":["edge"]',
    )


def too_few_samples(fx):
    sample = fx / PRACTICE / "tests/sample.jsonl"
    sample.write_text("".join(sample.read_text().splitlines(keepends=True)[:2]))


def too_few_hidden(fx):
    hidden = fx / PRACTICE / "tests/hidden.jsonl"
    hidden.write_text("".join(hidden.read_text().splitlines(keepends=True)[:5]))


def no_edge_test(fx):
    edit(fx / PRACTICE / "tests/hidden.jsonl", '"tags":["edge"]', '"tags":[]')


def hidden_too_big(fx):
    hidden = fx / PRACTICE / "tests/hidden.jsonl"
    hidden.write_text(hidden.read_text() + "\n" * 1_000_001)


def duplicate_test_ids(fx):
    edit(fx / PRACTICE / "tests/sample.jsonl", '"id":"s1"', '"id":"h01"')


def first_example_not_sample_one(fx):
    edit(fx / PRACTICE / "problem.yaml", "nums = [1, 2, 4]", "nums = [9]")


def compare_custom(fx):
    edit(fx / PRACTICE / "problem.yaml", "compare: exact", "compare: custom")


# --- problems: solutions -------------------------------------------------------------------


def solution_wrong(fx):
    edit(fx / PRACTICE / "solution.py", "x % 2 == 0", "x % 2 == 1")


def solution_does_not_compile(fx):
    (fx / PRACTICE / "solution.py").write_text("def count_evens(:\n")


def solution_over_time_share(fx):  # limit is 100 ms, so 0.3 x is 30 ms
    solution = fx / PRACTICE / "solution.py"
    solution.write_text(
        "import time\n\n\ndef count_evens(nums):\n"
        "    if len(nums) > 1000:  # only the stress test is slow\n"
        "        time.sleep(0.05)\n"
        "    return sum(1 for x in nums if x % 2 == 0)\n"
    )


def brute_disagrees(fx):
    edit(fx / PRACTICE / "brute.py", "    return n", "    return n + 1")


def brute_required_for_medium(fx):
    edit(fx / PRACTICE / "problem.yaml", "difficulty: easy", "difficulty: medium")
    (fx / PRACTICE / "brute.py").unlink()


def wrong_solution_passes(fx):
    shutil.copy(fx / PRACTICE / "solution.py", fx / PRACTICE / "wrong/fine.py")


def wrong_solution_does_not_compile(fx):
    (fx / PRACTICE / "wrong/broken.py").write_text("def count_evens(:\n")


def slow_solution_is_fast(fx):
    shutil.copy(fx / PRACTICE / "solution.py", fx / PRACTICE / "slow/sleeps.py")


def slow_without_stress_tests(fx):
    edit(fx / PRACTICE / "tests/gen.py", '"stress"', '"big"')
    edit(fx / PRACTICE / "tests/hidden.jsonl", '"stress"', '"big"')


def starter_solves_it(fx):
    def change(problem):
        problem["starter"]["python"] = (fx / PRACTICE / "solution.py").read_text()

    patch_yaml(fx / PRACTICE / "problem.yaml", change)


def starter_does_not_compile(fx):
    def change(problem):
        problem["starter"]["python"] = "def count_evens(:\n"

    patch_yaml(fx / PRACTICE / "problem.yaml", change)


CASES = {
    # rule: expected message fragment, and how to break the fixture
    "prerequisite is unknown": ("unknown prerequisites", unknown_prerequisite),
    "prerequisites form a cycle": ("prerequisite cycle", prerequisite_cycle),
    "lesson id is not a subtopic": ("not in content/index/subtopics.json", lesson_not_in_index),
    "subtopic has no lesson": ("missing lessons", missing_lesson),
    "lesson violates its schema": ("est_minutes", lesson_schema),
    "block ids repeat": ("duplicate block ids", duplicate_block_ids),
    "code_sample output differs": ("block f02", code_sample_output),
    "predict_output differs": ("block f05", predict_output_mismatch),
    "runnable code_sample crashes": ("block f02: RE", runnable_sample_crashes),
    "code_exercise solution fails": ("block f06: solution", exercise_solution_fails),
    "code_exercise starter passes": ("block f06: starter already passes", exercise_starter_passes),
    "fewer than 3 graded blocks": ("at least 3 graded blocks, has 1", too_few_graded_blocks),
    "min_items above graded blocks": ("at least 4 graded blocks", min_items_above_graded),
    "lesson problem is unknown": ("unknown problem nope", lesson_unknown_problem),
    "problem_ref not in practice/extra": (
        "problem_ref count-evens is not in",
        problem_ref_not_listed,
    ),
    "problem of another subtopic": (
        "belongs to py.core.variables_types",
        problem_of_another_subtopic,
    ),
    "published lesson, draft problem": (
        "links draft problem count-evens",
        published_lesson_links_draft_problem,
    ),
    "practice problem not in lesson": (
        "practice problem count-evens is not in",
        practice_problem_not_in_lesson,
    ),
    "mastery_check item is unknown": ("unknown item Q999", mastery_unknown_item),
    "mastery_check level mismatch": ("Q902 has difficulty 2", mastery_wrong_level),
    "level-2 write_code item missing": ("level-2 write_code", missing_level2_write_code),
    "no level-2 write_code item in the checks": (
        "needs a level-2 write_code item in content/checks",
        no_level2_write_code_in_checks,
    ),
    "check problem with 4 hidden tests": (
        "hidden has 4 tests",
        check_problem_has_four_hidden_tests,
    ),
    "extra check item not merged": ("not merged", extra_item_not_merged),
    "extra checks file misnamed": ("checks_extra/<subtopic_id>.yaml", extra_file_misnamed),
    "write_code item, unknown problem": ("unknown problem nope", check_item_unknown_problem),
    "write_code item, not a check problem": ("must be kind check", check_item_problem_not_a_check),
    "check item ids repeat": ("also appears in", duplicate_check_item_ids),
    "checks file misnamed": ("checks/<subtopic_id>.yaml", checks_file_misnamed),
    "problem violates its schema": ("difficulty", problem_schema),
    "problem directory name": ("directory name must equal", problem_directory_name),
    "secondary subtopic unknown": ("unknown subtopic nope.x", unknown_secondary_subtopic),
    "hidden file missing": ("missing hidden file", missing_hidden_file),
    "hidden tests are stale": ("stale", stale_hidden),
    "fewer than 3 samples": ("sample has 2 tests", too_few_samples),
    "fewer than 8 hidden tests": ("hidden has 5 tests", too_few_hidden),
    "no edge test": ("tagged 'edge'", no_edge_test),
    "hidden file over 1 MB": ("exceed", hidden_too_big),
    "test ids repeat": ("not unique", duplicate_test_ids),
    "first example is not sample 1": (
        "examples[0] must be sample test 1",
        first_example_not_sample_one,
    ),
    "compare custom": ("compare custom is not supported", compare_custom),
    "solution is wrong": ("solution WA", solution_wrong),
    "solution does not compile": ("solution CE", solution_does_not_compile),
    "solution over 0.3 x time_ms": ("over 0.3 x time_ms", solution_over_time_share),
    "brute force disagrees": ("disagrees with brute.py", brute_disagrees),
    "brute force missing for medium": ("brute.py is required", brute_required_for_medium),
    "wrong solution passes": ("fine.py passes every hidden test", wrong_solution_passes),
    "wrong solution does not compile": (
        "broken.py does not compile",
        wrong_solution_does_not_compile,
    ),
    "starter solves the problem": ("starter code already passes", starter_solves_it),
    "starter does not compile": ("starter code does not compile", starter_does_not_compile),
}
SLOW_CASES = {
    "slow solution is fast": ("must exceed 3 x time_ms", slow_solution_is_fast),
    "slow solution without stress tests": (
        "needs hidden tests tagged 'stress'",
        slow_without_stress_tests,
    ),
}


def test_good_fixture_is_clean(fx):
    assert errors_of(fx, keep_slow=True) == []


def test_check_problem_needs_only_one_sample(fx):
    sample = fx / CHECK_PROBLEM / "tests/sample.jsonl"
    sample.write_text(sample.read_text().splitlines(keepends=True)[0])
    assert errors_of(fx) == []


def test_merged_extra_item_is_accepted(fx):
    item = load_yaml(fx / CHECKS)["items"][0]
    (fx / "checks_extra").mkdir()
    (fx / "checks_extra" / f"{SUB}.yaml").write_text(
        dump_yaml({"subtopic_id": SUB, "items": [item]}), encoding="utf-8"
    )
    assert errors_of(fx) == []


def test_draft_lesson_needs_no_level2_write_code(fx):
    patch_yaml(fx / CHECKS, lambda checks: checks.update(items=checks["items"][:1]))
    patch_yaml(fx / LESSON, lambda lesson: lesson.update(status="draft"))
    assert not any("level-2 write_code" in e for e in errors_of(fx))


@pytest.mark.parametrize(("expected", "break_it"), CASES.values(), ids=CASES.keys())
def test_rule_is_enforced(fx, expected, break_it):
    break_it(fx)
    errors = errors_of(fx)
    assert any(expected in e for e in errors), errors


@pytest.mark.parametrize(("expected", "break_it"), SLOW_CASES.values(), ids=SLOW_CASES.keys())
def test_slow_rules_are_enforced(fx, expected, break_it):
    break_it(fx)
    errors = errors_of(fx, keep_slow=True)
    assert any(expected in e for e in errors), errors


def test_public_bundle_blocks_rewrite_required(fx):
    edit(
        fx / PRACTICE / "problem.yaml",
        "source:\n  type: original",
        "source:\n  type: leetcode\n  lc: 1\n  rewrite_required: true",
    )
    assert errors_of(fx) == []  # fine for the personal build
    errors = errors_of(fx, public=True)
    assert any("rewrite_required" in e for e in errors), errors


def test_public_bundle_ignores_unpublished_problems(fx):
    edit(
        fx / PRACTICE / "problem.yaml",
        "source:\n  type: original",
        "source:\n  type: leetcode\n  lc: 1\n  rewrite_required: true",
    )
    edit(fx / PRACTICE / "problem.yaml", "status: published", "status: draft")
    patch_yaml(fx / LESSON, lambda lesson: lesson.update(status="validated"))
    assert errors_of(fx, public=True) == []


@pytest.mark.skipif(not pyodide_available(), reason="run `npm ci` in tools/pyodide-node")
class TestPyodideEngine:
    def test_good_fixture_passes_under_pyodide(self, fx):
        assert errors_of(fx, pyodide=True) == []

    def test_solution_that_only_fails_in_the_browser_runtime(self, fx):
        solution = fx / PRACTICE / "solution.py"
        solution.write_text(
            "import sys\n\n\ndef count_evens(nums):\n"
            "    if sys.platform == 'emscripten' and len(nums) > 1000:\n"
            "        return -1\n"
            "    return sum(1 for x in nums if x % 2 == 0)\n"
        )
        assert errors_of(fx) == []  # native is happy
        errors = errors_of(fx, pyodide=True)
        assert any("under Pyodide" in e for e in errors), errors
