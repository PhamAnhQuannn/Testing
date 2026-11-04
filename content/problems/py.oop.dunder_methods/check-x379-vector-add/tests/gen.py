"""Inputs of check-x379-vector-add; `expected` is recorded from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2], [10, 20]]},
    {"id": "s2", "args": [[0, 0], [0, 0]]},
    {"id": "s3", "args": [[-1, 5], [1, -5]]},
]

HIDDEN = [
    {"id": "h01", "args": [[0, 0], [0, 0]], "tags": ["edge"]},
    {"id": "h02", "args": [[3, 4], [0, 0]], "tags": []},
    {"id": "h03", "args": [[-7, -2], [-3, 9]], "tags": []},
    {"id": "h04", "args": [[100, 200], [300, 400]], "tags": []},
    {"id": "h05", "args": [[1, -1], [-1, 1]], "tags": ["edge"]},
    {"id": "h06", "args": [[12345, 6], [5, 94]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
