"""Inputs of check-x392-scaled-factory.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [2, [1, 2]]}

HIDDEN = [
    {"id": "h01", "args": [3, []], "tags": ["edge"]},
    {"id": "h02", "args": [0, [4, 5]], "tags": []},
    {"id": "h03", "args": [1, [10]], "tags": []},
    {"id": "h04", "args": [-2, [1, -1, 0]], "tags": []},
    {"id": "h05", "args": [5, list(range(10))], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
