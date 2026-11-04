"""Inputs of check-collatz-longest: `expected` is recorded from solution.py by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [10]},
    {"id": "s2", "args": [1]},
    {"id": "s3", "args": [3]},
]

HIDDEN = [
    {"id": "h01", "args": [1], "tags": ["edge"]},
    {"id": "h02", "args": [2], "tags": []},
    {"id": "h03", "args": [3], "tags": []},
    {"id": "h04", "args": [7], "tags": []},
    {"id": "h05", "args": [9], "tags": []},
    {"id": "h06", "args": [27], "tags": []},
    {"id": "h07", "args": [30], "tags": []},
    {"id": "h08", "args": [100], "tags": []},
    {"id": "h09", "args": [500], "tags": []},
    {"id": "h10", "args": [1000], "tags": []},
    {"id": "h11", "args": [3000], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
