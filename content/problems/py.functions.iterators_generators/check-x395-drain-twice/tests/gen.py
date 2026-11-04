"""Inputs of check-x395-drain-twice; `expected` is recorded from solution.py."""

SAMPLE = {"id": "s1", "args": [4]}

HIDDEN = [
    {"id": "h01", "args": [0], "tags": ["edge"]},
    {"id": "h02", "args": [1], "tags": ["edge"]},
    {"id": "h03", "args": [2], "tags": []},
    {"id": "h04", "args": [5], "tags": []},
    {"id": "h05", "args": [10], "tags": []},
    {"id": "h06", "args": [25], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
