"""Inputs of check-to-base: `expected` is recorded from solution.py by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [255, 16]},
    {"id": "s2", "args": [10, 2]},
    {"id": "s3", "args": [0, 7]},
]

HIDDEN = [
    {"id": "h01", "args": [0, 2], "tags": ["edge"]},
    {"id": "h02", "args": [1, 2], "tags": []},
    {"id": "h03", "args": [5, 2], "tags": []},
    {"id": "h04", "args": [255, 16], "tags": []},
    {"id": "h05", "args": [-255, 16], "tags": []},
    {"id": "h06", "args": [35, 36], "tags": []},
    {"id": "h07", "args": [36, 36], "tags": []},
    {"id": "h08", "args": [100, 10], "tags": []},
    {"id": "h09", "args": [-1, 3], "tags": []},
    {"id": "h10", "args": [123456789, 36], "tags": []},
    {"id": "h11", "args": [1099511627776, 2], "tags": []},
    {"id": "h12", "args": [1000, 8], "tags": []},
    {"id": "h13", "args": [9, 9], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
