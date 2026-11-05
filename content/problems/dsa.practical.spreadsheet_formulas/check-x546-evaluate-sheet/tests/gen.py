"""Inputs of check-x546-evaluate-sheet; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [{"A": "=B", "B": "=A", "C": 5}]},
    {"id": "s2", "args": [{"A": 3, "B": "=A+A", "C": "=A+B"}]},
    {"id": "s3", "args": [{"A": 1, "B": "=A+C", "C": "=B", "D": "=A+B"}]},
]


def _chain(n):
    cells = {"C0": 1}
    for i in range(1, n):
        cells[f"C{i}"] = f"=C{i - 1}+C{i - 1}" if i % 2 else f"=C{i - 1}"
    return cells


def _long_cycle(n):
    cells = {f"N{i}": f"=N{(i + 1) % n}" for i in range(n)}
    cells["OK"] = 9
    cells["BAD"] = "=N0+OK"
    return cells


HIDDEN = [
    {"id": "h01", "args": [{"A": 5}], "tags": ["edge"]},
    {"id": "h02", "args": [{"A": "=A"}], "tags": ["edge"]},
    {"id": "h03", "args": [{"A": "=B", "B": "=A"}], "tags": ["edge"]},
    {"id": "h04", "args": [{"A": 1, "B": "=A", "C": "=B"}], "tags": ["edge"]},
    {
        "id": "h05",
        "args": [{"A": "=B", "B": "=C", "C": "=B", "D": "=A+E", "E": 4}],
        "tags": ["edge"],
    },
    {"id": "h06", "args": [{"A": 2, "B": "=A+A", "C": "=B+A", "D": 1, "E": "=D+D"}], "tags": []},
    {"id": "h07", "args": [{"A": "=B+C", "B": "=A", "C": 7, "D": "=C+C"}], "tags": []},
    {"id": "h08", "args": [{"A": "=B+C", "B": "=D", "C": "=D", "D": 3}], "tags": []},
    {"id": "h09", "args": [_chain(60)], "tags": []},
    {"id": "h10", "args": [_long_cycle(40)], "tags": []},
    {
        "id": "h11",
        "args": [{"A": 1, "B": "=A+C", "C": "=D", "D": "=B", "E": "=A+A", "F": "=E+D"}],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
