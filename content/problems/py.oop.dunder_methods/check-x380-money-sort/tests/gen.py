"""Inputs of check-x380-money-sort; `expected` is recorded from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[1250, 505, 99]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [[100, 100, 5]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[0]], "tags": ["edge"]},
    {"id": "h03", "args": [[7]], "tags": []},
    {"id": "h04", "args": [[100, 100, 5]], "tags": []},
    {"id": "h05", "args": [[99999, 1, 50000, 250]], "tags": []},
    {"id": "h06", "args": [[5, 4, 3, 2, 1, 0]], "tags": []},
    {"id": "h07", "args": [[1000, 1000, 1000]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
