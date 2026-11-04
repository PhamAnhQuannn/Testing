"""Inputs of check-x394-first-evens; `expected` is recorded from solution.py."""

SAMPLE = {"id": "s1", "args": [[1, 2, 3, 4, 5, 6, 7, 8], 3]}

HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 3, 5], 2], "tags": ["edge"]},
    {"id": "h03", "args": [[2, 4, 6, 8], 0], "tags": ["edge"]},
    {"id": "h04", "args": [[2, 4], 5], "tags": []},
    {"id": "h05", "args": [[7, 10, 3, 12, 5, 14], 2], "tags": []},
    {"id": "h06", "args": [[-4, -3, 0, 1, 6], 3], "tags": []},
    {"id": "h07", "args": [list(range(1, 50)), 4], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
