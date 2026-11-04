"""Inputs of check-x404-nested-scopes; `expected` is recorded from solution.py."""

SAMPLE = {"id": "s1", "args": [["a", "b"], True]}

HIDDEN = [
    {"id": "h01", "args": [[], False], "tags": ["edge"]},
    {"id": "h02", "args": [[], True], "tags": ["edge"]},
    {"id": "h03", "args": [["a"], False], "tags": []},
    {"id": "h04", "args": [["a", "b"], False], "tags": []},
    {"id": "h05", "args": [["a", "b"], True], "tags": []},
    {"id": "h06", "args": [["x", "y", "z"], True], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
