"""Inputs of check-x400-fib-stats.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [10]},
    {"id": "s2", "args": [0]},
    {"id": "s3", "args": [3]},
]

HIDDEN = [
    {"id": "h01", "args": [0], "tags": ["edge"]},
    {"id": "h02", "args": [1], "tags": ["edge"]},
    {"id": "h03", "args": [2], "tags": []},
    {"id": "h04", "args": [5], "tags": []},
    {"id": "h05", "args": [10], "tags": []},
    {"id": "h06", "args": [20], "tags": []},
    {"id": "h07", "args": [30], "tags": []},
    {"id": "h08", "args": [50], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
