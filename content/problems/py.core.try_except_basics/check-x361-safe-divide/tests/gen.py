"""Inputs of check-x361-safe-divide; expected is recorded from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[[7, 2], [1, 0]]]},
    {"id": "s2", "args": [[[10, 5], [9, 3], [8, 4]]]},
    {"id": "s3", "args": [[[0, 0], [5, 0]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[[0, 5]]], "tags": []},
    {"id": "h03", "args": [[[-7, 2], [7, -2]]], "tags": []},
    {"id": "h04", "args": [[[1, 0], [2, 0], [3, 0]]], "tags": []},
    {"id": "h05", "args": [[[100, 7], [5, 0], [0, 1], [-9, 3]]], "tags": []},
    {"id": "h06", "args": [[[1, 2], [1, 3], [1, 0], [1, 1]]], "tags": []},
    {"id": "h07", "args": [[[-5, 0], [0, -3]]], "tags": []},
    {"id": "h08", "args": [[[12, 4], [13, 4], [14, 4], [15, 0]]], "tags": []},
    {"id": "h09", "args": [[[1000000, 3], [2, 0]]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
