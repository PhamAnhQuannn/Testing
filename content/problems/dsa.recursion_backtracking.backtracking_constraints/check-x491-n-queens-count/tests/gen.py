"""Inputs of check-x491-n-queens-count; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [4]},
    {"id": "s2", "args": [1]},
    {"id": "s3", "args": [5]},
]

HIDDEN = [
    {"id": "h01", "args": [1], "tags": ["edge"]},
    {"id": "h02", "args": [2], "tags": ["edge"]},
    {"id": "h03", "args": [3], "tags": ["edge"]},
    {"id": "h04", "args": [4], "tags": []},
    {"id": "h05", "args": [5], "tags": []},
    {"id": "h06", "args": [6], "tags": []},
    {"id": "h07", "args": [7], "tags": []},
    {"id": "h08", "args": [8], "tags": []},
    {"id": "h09", "args": [9], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
