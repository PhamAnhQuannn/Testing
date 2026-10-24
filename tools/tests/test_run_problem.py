import pytest

from common import CONTENT, load_yaml
from run_problem import load_tests, run_native

RANSOM_NOTE = CONTENT / "problems/py.datastructs.dict/ransom-note"
IO = {"mode": "function", "entry": "f"}
PROBLEM = load_yaml(RANSOM_NOTE / "problem.yaml")


def test_time_limit_kills_the_run_and_skips_the_remaining_tests():
    code = "def f(x):\n    while x:\n        pass\n    return 1"
    tests = [
        {"id": "a", "args": [0], "expected": 1},
        {"id": "b", "args": [1]},
        {"id": "c", "args": [0]},
    ]
    run = run_native(code, IO, tests, time_limit_ms=200)
    assert [(r["id"], r["verdict"]) for r in run["results"]] == [("a", "AC"), ("b", "TLE")]
    assert run["verdict"] == "TLE"


def test_syntax_error_is_a_single_ce_result():
    run = run_native("def f(:", IO, [{"id": "a", "args": []}], time_limit_ms=1000)
    assert [r["verdict"] for r in run["results"]] == ["CE"]


def test_crash_of_the_runner_is_reported():
    code = "import os\ndef f():\n    os._exit(3)"
    run = run_native(code, IO, [{"id": "a", "args": [], "expected": 1}], time_limit_ms=1000)
    assert run["verdict"] == "RE"


@pytest.mark.parametrize(
    ("solution", "failing"),
    [
        ("solution.py", set()),
        ("brute.py", {"h11"}),  # correct but quadratic: times out on the first stress test
        ("wrong/no_count.py", {"s2", "h05", "h09", "h12"}),
        ("wrong/off_by_one.py", {"s3", "h04", "h06", "h07", "h08", "h11"}),
    ],
)
def test_ransom_note_variants(solution, failing):
    tests = load_tests(RANSOM_NOTE, PROBLEM, "all")
    code = (RANSOM_NOTE / solution).read_text(encoding="utf-8")
    run = run_native(code, PROBLEM["io"], tests, PROBLEM["limits"]["time_ms"])
    got = {r["id"] for r in run["results"] if r["verdict"] != "AC"}
    assert got == failing
