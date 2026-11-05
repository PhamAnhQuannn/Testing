"""Inputs of check-x545-cell-value; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [{"A": 3, "B": "=A+A", "C": "=A+B"}, "C"]},
    {"id": "s2", "args": [{"A": 7}, "A"]},
    {"id": "s3", "args": [{"A": 1, "B": 2, "C": "=A+B", "D": "=C+C+A"}, "D"]},
]


def _chain(n):
    cells = {"C0": 1}
    for i in range(1, n):
        cells[f"C{i}"] = f"=C{i - 1}+C{i - 1}" if i % 2 else f"=C{i - 1}"
    return cells, f"C{n - 1}"


def _fib(n):
    cells = {"F0": 0, "F1": 1}
    for i in range(2, n):
        cells[f"F{i}"] = f"=F{i - 1}+F{i - 2}"
    return cells, f"F{n - 1}"


def _wide(n):
    cells = {f"X{i}": i for i in range(n)}
    cells["SUM"] = "=" + "+".join(f"X{i}" for i in range(n))
    return cells, "SUM"


_c, _t = _chain(60)
_f, _ft = _fib(40)
_w, _wt = _wide(30)

HIDDEN = [
    {"id": "h01", "args": [{"A": 5}, "A"], "tags": ["edge"]},
    {"id": "h02", "args": [{"A": 0, "B": "=A"}, "B"], "tags": ["edge"]},
    {"id": "h03", "args": [{"A": 2, "B": "=A", "C": "=B"}, "C"], "tags": ["edge"]},
    {"id": "h04", "args": [{"A": -3, "B": 10, "C": "=A+B"}, "C"], "tags": []},
    {"id": "h05", "args": [{"A": 3, "B": "=A+A", "C": "=A+B", "D": 100}, "B"], "tags": []},
    {
        "id": "h06",
        "args": [{"A": 1, "B": "=A+A", "C": "=B+B", "D": "=C+C", "E": "=D+D"}, "E"],
        "tags": [],
    },
    {"id": "h07", "args": [_c, _t], "tags": []},
    {"id": "h08", "args": [_f, _ft], "tags": []},
    {"id": "h09", "args": [_w, _wt], "tags": []},
    {
        "id": "h10",
        "args": [{"A1": 4, "B1": "=A1+A1+A1", "C1": "=B1+A1", "D1": "=C1+B1+A1"}, "D1"],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
