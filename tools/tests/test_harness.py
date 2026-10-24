import pytest

import harness


def run(code, io, *tests):
    return list(harness.run_tests(code, io, [{"id": f"t{i}", **t} for i, t in enumerate(tests)]))


def verdicts(results):
    return [r["verdict"] for r in results]


FUNCTION = {"mode": "function", "entry": "f"}


def test_function_exact_distinguishes_bool_from_int():
    results = run("def f(x):\n    return x == 1", FUNCTION, {"args": [1], "expected": True},
                  {"args": [1], "expected": 1})  # fmt: skip
    assert verdicts(results) == ["AC", "WA"]


def test_function_tuple_equals_list():
    assert verdicts(
        run("def f():\n    return (1, 2)", FUNCTION, {"args": [], "expected": [1, 2]})
    ) == ["AC"]


@pytest.mark.parametrize(
    ("compare", "expected", "verdict"),
    [("exact", [2, 1], "WA"), ("unordered", [2, 1], "AC"), ("unordered", [2, 2], "WA")],
)
def test_compare_modes(compare, expected, verdict):
    io = FUNCTION | {"compare": compare}
    assert verdicts(run("def f():\n    return [1, 2]", io, {"args": [], "expected": expected})) == [
        verdict
    ]


def test_float_tolerance():
    io = FUNCTION | {"compare": "float_tol"}
    assert verdicts(run("def f():\n    return 0.1 + 0.2", io, {"args": [], "expected": 0.3})) == [
        "AC"
    ]


def test_list_node_in_and_out():
    io = {
        "mode": "function",
        "entry": "f",
        "params": [{"name": "head", "type": "list_node"}],
        "returns": "list_node",
    }
    code = (
        "def f(head):\n"
        "    prev = None\n"
        "    while head:\n"
        "        head.next, prev, head = prev, head, head.next\n"
        "    return prev"
    )
    assert verdicts(run(code, io, {"args": [[1, 2, 3]], "expected": [3, 2, 1]})) == ["AC"]


def test_tree_node_in_and_out():
    io = {
        "mode": "function",
        "entry": "f",
        "params": [{"name": "root", "type": "tree_node"}],
        "returns": "tree_node",
    }
    code = "def f(root):\n    root.left, root.right = root.right, root.left\n    return root"
    test = {"args": [[1, 2, 3, None, 4]], "expected": [1, 3, 2, None, None, None, 4]}
    assert verdicts(run(code, io, test)) == ["AC"]


def test_inplace_compares_the_mutated_argument():
    io = {
        "mode": "inplace",
        "entry": "f",
        "params": [{"name": "a", "type": "list"}],
        "inplace_arg": 0,
    }
    assert verdicts(
        run("def f(a):\n    a.reverse()", io, {"args": [[1, 2]], "expected": [2, 1]})
    ) == ["AC"]


def test_class_ops():
    io = {"mode": "class_ops"}
    code = (
        "class Counter:\n"
        "    def __init__(self):\n"
        "        self.n = 0\n"
        "    def inc(self):\n"
        "        self.n += 1\n"
        "        return self.n"
    )
    test = {"ops": ["Counter", "inc", "inc"], "args": [[], [], []], "expected": [None, 1, 2]}
    assert verdicts(run(code, io, test)) == ["AC"]


def test_stdout_mode_reads_stdin_and_ignores_trailing_whitespace():
    code = "name = input()\nprint('hi', name, end='  \\n\\n')"
    results = run(code, {"mode": "stdout"}, {"stdin": "An\n", "expected": "hi An"})
    assert verdicts(results) == ["AC"]


def test_runtime_error_compile_error_and_exit():
    results = run("def f():\n    return 1 / 0", FUNCTION, {"args": [], "expected": 1})
    assert (results[0]["verdict"], results[0]["error"]) == (
        "RE",
        "ZeroDivisionError: division by zero",
    )
    assert verdicts(run("def f(:", FUNCTION, {"args": [], "expected": 1})) == ["CE"]
    assert verdicts(run("raise SystemExit(1)", {"mode": "stdout"}, {"expected": ""})) == ["RE"]


def test_state_does_not_leak_between_tests():
    code = "seen = []\ndef f():\n    seen.append(1)\n    return len(seen)"
    results = run(code, FUNCTION, {"args": [], "expected": 1}, {"args": [], "expected": 1})
    assert verdicts(results) == ["AC", "AC"]


def test_test_without_expected_records_the_output():
    result = run("def f(x):\n    print('log')\n    return x * 2", FUNCTION, {"args": [4]})[0]
    assert (result["verdict"], result["got"], result["stdout"]) == ("AC", 8, "log\n")


def test_custom_compare_is_rejected_until_implemented():
    io = FUNCTION | {"compare": "custom"}
    assert verdicts(run("def f():\n    return 1", io, {"args": [], "expected": 1})) == ["RE"]
