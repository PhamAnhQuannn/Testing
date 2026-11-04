"""Inputs of check-x413-eval-expr.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [["add", 1, ["mul", 2, 3]]]},
    {"id": "s2", "args": [5]},
    {"id": "s3", "args": [["neg", ["add", 2, 3]]]},
]

HIDDEN = [
    {"id": "h01", "args": [0], "tags": ["edge"]},
    {"id": "h02", "args": [["add"]], "tags": ["edge"]},
    {"id": "h03", "args": [["mul"]], "tags": ["edge"]},
    {"id": "h04", "args": [["foo", 1, 2]], "tags": ["edge"]},
    {"id": "h05", "args": ["text"], "tags": ["edge"]},
    {"id": "h06", "args": [["neg", 1, 2]], "tags": ["edge"]},
    {"id": "h07", "args": [["add", 1, 2, 3, 4]], "tags": []},
    {"id": "h08", "args": [["mul", 2, 3, 4]], "tags": []},
    {"id": "h09", "args": [["if", 1, 10, 20]], "tags": []},
    {"id": "h10", "args": [["if", ["add", 1, -1], 10, 20]], "tags": []},
    {
        "id": "h11",
        "args": [["add", ["mul", 2, ["neg", 3]], ["if", 0, 1, ["add", 4, 5]]]],
        "tags": [],
    },
    {"id": "h12", "args": [["add", "x", ["bad"], 7]], "tags": []},
    {"id": "h13", "args": [["if", 1, 2]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
