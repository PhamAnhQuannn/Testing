"""Inputs of check-x397-pairs-with-sum.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4, 5], 6]},
    {"id": "s2", "args": [[3, 3, 3], 6]},
    {"id": "s3", "args": [[1, 2], 10]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 5], "tags": ["edge"]},
    {"id": "h02", "args": [[7], 7], "tags": ["edge"]},
    {"id": "h03", "args": [[0, 0, 0, 0], 0], "tags": []},
    {"id": "h04", "args": [[-3, 3, 0, 5, -5], 0], "tags": []},
    {"id": "h05", "args": [[5, 1, 4, 2, 3], 6], "tags": []},
    {"id": "h06", "args": [[2, 2, 2, 4, 4], 6], "tags": []},
    {"id": "h07", "args": [[10, 20, 30], 100], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
