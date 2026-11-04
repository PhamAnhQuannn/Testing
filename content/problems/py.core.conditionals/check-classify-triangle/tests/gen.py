"""Inputs of check-classify-triangle: `expected` is recorded from solution.py by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [3, 4, 5]},
    {"id": "s2", "args": [2, 2, 2]},
    {"id": "s3", "args": [1, 2, 3]},
]

HIDDEN = [
    {"id": "h01", "args": [5, 4, 3], "tags": ["edge"]},
    {"id": "h02", "args": [1, 1, 1], "tags": []},
    {"id": "h03", "args": [2, 2, 3], "tags": []},
    {"id": "h04", "args": [1, 2, 3], "tags": []},
    {"id": "h05", "args": [0, 1, 1], "tags": []},
    {"id": "h06", "args": [-3, 4, 5], "tags": []},
    {"id": "h07", "args": [5, 5, 10], "tags": []},
    {"id": "h08", "args": [7, 10, 5], "tags": []},
    {"id": "h09", "args": [6, 6, 6], "tags": []},
    {"id": "h10", "args": [5, 12, 13], "tags": []},
    {"id": "h11", "args": [10, 6, 8], "tags": []},
    {"id": "h12", "args": [100000, 100000, 1], "tags": []},
    {"id": "h13", "args": [3, 3, 5], "tags": []},
    {"id": "h14", "args": [1, 1, 2], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
