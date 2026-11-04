"""Inputs of check-x437-merge-k. `expected` is recorded from solution.py by tools/gen_hidden.py."""

SAMPLE = {"id": "s1", "args": [[[1, 4, 5], [1, 3, 4], [2, 6]]]}
SAMPLES = [
    SAMPLE,
    {"id": "s2", "args": [[[], [1], []]]},
    {"id": "s3", "args": [[[-3, 0, 5], [-4, 0, 0, 9]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[[]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[7]]], "tags": []},
    {"id": "h04", "args": [[[1, 2, 3], [4, 5, 6]]], "tags": []},
    {"id": "h05", "args": [[[4, 5, 6], [1, 2, 3]]], "tags": []},
    {"id": "h06", "args": [[[2, 2, 2], [2, 2], [2]]], "tags": []},
    {"id": "h07", "args": [[[-10, -5], [-7, 0, 3], [], [1, 1, 100]]], "tags": []},
    {"id": "h08", "args": [[[i * 5 + k for i in range(40)] for k in range(5)]], "tags": []},
    {"id": "h09", "args": [[[1], [1], [1], [0]]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
