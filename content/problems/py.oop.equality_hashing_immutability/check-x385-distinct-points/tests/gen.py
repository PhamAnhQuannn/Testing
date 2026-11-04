"""Inputs of check-x385-distinct-points.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[[1, 2], [1, 2], [2, 1]]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[[0, 0]]], "tags": []},
    {"id": "h03", "args": [[[0, 0], [0, 0], [0, 0], [5, 5]]], "tags": []},
    {"id": "h04", "args": [[[1, 2], [2, 1], [1, 2], [2, 1]]], "tags": []},
    {"id": "h05", "args": [[[-1, 3], [-1, 3], [3, -1], [-1, -3]]], "tags": []},
    {"id": "h06", "args": [[[1, 1], [1, 2], [1, 3], [2, 1], [1, 1]]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
