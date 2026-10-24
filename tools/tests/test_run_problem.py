import sys

import pytest

from common import CONTENT, load_yaml
from run_problem import (
    engine_limit_ms,
    load_tests,
    main,
    parse_result,
    pyodide_available,
    run_engine,
    run_native,
)

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


def test_quadratic_brute_force_times_out_on_the_first_stress_test():
    tests = load_tests(RANSOM_NOTE, PROBLEM, "hidden")
    code = (RANSOM_NOTE / "brute.py").read_text(encoding="utf-8")
    run = run_native(code, PROBLEM["io"], tests, time_limit_ms=100)  # tight: machine independent
    assert [r["id"] for r in run["results"] if r["verdict"] != "AC"] == ["h11"]
    assert run["results"][-1]["verdict"] == "TLE"


def test_every_result_has_the_full_shape_even_for_compile_errors():
    run = run_native("def f(:", IO, [{"id": "a", "args": []}], time_limit_ms=1000)
    assert set(run["results"][0]) == {
        "id",
        "verdict",
        "got",
        "error",
        "stdout",
        "stderr",
        "elapsed_ms",
    }


def test_cli_reports_a_syntax_error_instead_of_crashing(tmp_path, monkeypatch, capsys):
    (tmp_path / "wrong").mkdir()
    (tmp_path / "wrong/bad.py").write_text("def can_construct(:\n")
    for name in ("problem.yaml", "tests"):
        source = RANSOM_NOTE / name
        (tmp_path / name).symlink_to(source)
    monkeypatch.setattr(sys, "argv", ["run_problem", str(tmp_path), "--solution", "wrong/bad.py"])
    assert main() == 1
    assert "verdict: CE" in capsys.readouterr().out


def test_learner_code_writing_to_file_descriptor_1_cannot_corrupt_the_results():
    code = (
        "import os, sys\n"
        "def f():\n"
        "    os.write(1, b'garbage\\n{not json\\n')\n"
        "    sys.__stdout__.write('more garbage\\n')\n"
        "    sys.__stdout__.flush()\n"
        "    return 1\n"
    )
    tests = [{"id": "a", "args": [], "expected": 1}, {"id": "b", "args": [], "expected": 1}]
    run = run_native(code, IO, tests, time_limit_ms=1000)
    assert [r["verdict"] for r in run["results"]] == ["AC", "AC"]


def test_parse_result_ignores_lines_that_are_not_results():
    assert parse_result(b"garbage") is None
    assert parse_result(b'{"unrelated": 1}') is None
    assert parse_result(b'{"verdict": "AC"}') == {"verdict": "AC"}


needs_pyodide = pytest.mark.skipif(
    not pyodide_available(), reason="run `npm ci` in tools/pyodide-node"
)


@needs_pyodide
@pytest.mark.parametrize(
    ("solution", "failing"),
    [
        ("solution.py", set()),
        ("wrong/no_count.py", {"s2", "h05", "h09", "h12"}),
        ("wrong/off_by_one.py", {"s3", "h04", "h06", "h07", "h08", "h11"}),
    ],
)
def test_pyodide_engine_agrees_with_native(solution, failing):
    tests = load_tests(RANSOM_NOTE, PROBLEM, "all")
    code = (RANSOM_NOTE / solution).read_text(encoding="utf-8")
    run = run_engine("pyodide", code, PROBLEM["io"], tests, engine_limit_ms(PROBLEM, "pyodide"))
    assert {r["id"] for r in run["results"] if r["verdict"] != "AC"} == failing


@needs_pyodide
def test_pyodide_engine_kills_an_infinite_loop():
    code = "def f(x):\n    while x:\n        pass\n    return 1"
    tests = [
        {"id": "a", "args": [0], "expected": 1},
        {"id": "b", "args": [1]},
        {"id": "c", "args": [0]},
    ]
    run = run_engine("pyodide", code, IO, tests, time_limit_ms=300)
    assert [(r["id"], r["verdict"]) for r in run["results"]] == [("a", "AC"), ("b", "TLE")]


@needs_pyodide
def test_pyodide_engine_reports_compile_errors_and_runtime_errors():
    run = run_engine("pyodide", "def f(:", IO, [{"id": "a", "args": []}], 1000)
    assert [r["verdict"] for r in run["results"]] == ["CE"]
    code = "def f():\n    raise ValueError('boom')"
    run = run_engine("pyodide", code, IO, [{"id": "a", "args": [], "expected": 1}], 1000)
    assert run["results"][0]["verdict"] == "RE" and "boom" in run["results"][0]["error"]


def test_pyodide_limit_applies_the_time_multiplier():
    assert engine_limit_ms(PROBLEM, "native") == 1000
    assert engine_limit_ms(PROBLEM, "pyodide") == 3000
