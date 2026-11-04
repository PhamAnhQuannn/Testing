"""Inputs of check-x391-counted-calls.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[1, 2]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[7]], "tags": []},
    {"id": "h03", "args": [[5, 5, 5]], "tags": []},
    {"id": "h04", "args": [[-3, 0, 4, 10]], "tags": []},
    {"id": "h05", "args": [list(range(20))], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
