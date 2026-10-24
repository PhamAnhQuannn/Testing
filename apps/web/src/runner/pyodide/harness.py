"""Shared test harness: the single definition of "a solution passes a test".

Used by the Pyodide worker in the browser (it iterates `run_tests`) and by
`tools/run_problem.py --engine native` (it runs this file as a script and reads
JSON lines). Standard library only, so it runs unchanged in both.

Request (JSON on stdin when run as a script)::

    {"code": str, "io": {...problem.yaml io...}, "tests": [{...JSONL test...}]}

Each result is a dict ``{id, verdict, got, error, stdout, stderr, elapsed_ms}``
with verdict ``AC`` | ``WA`` | ``RE`` | ``CE``. TLE is decided by whoever owns
the watchdog, not by the harness. A test without ``expected`` is only executed
(verdict ``AC`` unless it raises); the test generator uses that to record outputs.
"""

import contextlib
import io as _io
import json
import math
import sys
import time

MAX_TEXT = 10_000
RECURSION_LIMIT = 1000


class ListNode:
    def __init__(self, val=0, next=None):  # noqa: A002 - LeetCode signature
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_list(values):
    head = None
    for val in reversed(values):
        head = ListNode(val, head)
    return head


def list_of(node):
    values = []
    while node is not None:
        values.append(node.val)
        node = node.next
    return values


def build_tree(values):
    """Level-order list with None holes, e.g. [1, None, 2] (LeetCode format)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = [root], 1
    for node in queue:
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = TreeNode(values[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def tree_of(root):
    values, queue = [], [root]
    for node in queue:
        if node is None:
            values.append(None)
        else:
            values.append(node.val)
            queue += [node.left, node.right]
    while values and values[-1] is None:
        values.pop()
    return values


TO_PYTHON = {"list_node": build_list, "tree_node": build_tree}
FROM_PYTHON = {"list_node": list_of, "tree_node": tree_of}


def _convert(table, kind, value):
    return table[kind](value) if kind in table else value


def _equal(a, b, tolerance):
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_equal(x, y, tolerance) for x, y in zip(a, b, strict=True))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_equal(a[k], b[k], tolerance) for k in a)
    if tolerance and isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-9)
    return a == b


def _canonical(value):
    return json.dumps(value, sort_keys=True, default=repr)


def matches(got, expected, compare="exact"):
    """Compare a result with the expected value according to `io.compare`."""
    if compare == "exact":
        return _equal(got, expected, tolerance=False)
    if compare == "float_tol":
        return _equal(got, expected, tolerance=True)
    if compare == "unordered":
        return sorted(map(_canonical, got)) == sorted(map(_canonical, expected))
    raise NotImplementedError(f"compare={compare!r} is not supported")


def _normalize_output(text):
    return "\n".join(line.rstrip() for line in text.rstrip().split("\n"))


def _build_args(params, values):
    if not params:  # lesson code_exercise declares no parameter types
        return list(values)
    return [_convert(TO_PYTHON, p.get("type"), v) for p, v in zip(params, values, strict=True)]


def _call(namespace, io, test):
    mode = io["mode"]
    if mode == "function":
        args = _build_args(io.get("params", []), test["args"])
        return _convert(FROM_PYTHON, io.get("returns"), namespace[io["entry"]](*args))
    if mode == "inplace":
        args = _build_args(io["params"], test["args"])
        namespace[io["entry"]](*args)
        index = io["inplace_arg"]
        return _convert(FROM_PYTHON, io["params"][index].get("type"), args[index])
    if mode == "class_ops":
        ops, args = test["ops"], test["args"]
        obj = namespace[ops[0]](*args[0])
        return [None] + [getattr(obj, op)(*a) for op, a in zip(ops[1:], args[1:], strict=True)]
    raise ValueError(f"unknown io.mode {mode!r}")


def _clip(text):
    return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + "\n...[truncated]"


def run_test(program, io, test):
    """Run one test against a compiled program and return its result dict."""
    out, err = _io.StringIO(), _io.StringIO()
    stdin, sys.stdin = sys.stdin, _io.StringIO(test.get("stdin", ""))
    verdict, got, error = "AC", None, ""
    started = time.perf_counter()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            namespace = {"__name__": "__main__", "ListNode": ListNode, "TreeNode": TreeNode}
            exec(program, namespace)  # noqa: S102 - running submitted code is the job
            got = out.getvalue() if io["mode"] == "stdout" else _call(namespace, io, test)
        if "expected" in test:
            if io["mode"] == "stdout":
                same = _normalize_output(got) == _normalize_output(test["expected"])
            else:
                same = matches(got, test["expected"], io.get("compare", "exact"))
            verdict = "AC" if same else "WA"
    except (Exception, SystemExit) as exc:  # user code may raise anything, even exit()
        verdict, error = "RE", f"{type(exc).__name__}: {exc}"
    finally:
        sys.stdin = stdin
    return {
        "id": test.get("id"),
        "verdict": verdict,
        "got": got,
        "error": _clip(error),
        "stdout": _clip(out.getvalue()),
        "stderr": _clip(err.getvalue()),
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
    }


def run_tests(code, io, tests):
    """Yield one result per test; a syntax error yields a single `CE` result."""
    sys.setrecursionlimit(RECURSION_LIMIT)
    try:
        program = compile(code, "<solution>", "exec")
    except SyntaxError as exc:
        yield {"id": None, "verdict": "CE", "error": f"{type(exc).__name__}: {exc}"}
        return
    for test in tests:
        yield run_test(program, io, test)


def main():
    request = json.load(sys.stdin)
    channel = sys.stdout  # run_test swaps sys.stdout while user code runs
    for result in run_tests(request["code"], request["io"], request["tests"]):
        channel.write(json.dumps(result, default=repr) + "\n")
        channel.flush()


if __name__ == "__main__":
    main()
