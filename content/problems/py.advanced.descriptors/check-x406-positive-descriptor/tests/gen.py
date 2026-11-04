"""Inputs of check-x406-positive-descriptor.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[5, -1, 3]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [[0]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[0]], "tags": ["edge"]},
    {"id": "h03", "args": [[1]], "tags": []},
    {"id": "h04", "args": [[-5, -2]], "tags": []},
    {"id": "h05", "args": [[3, 2, 1]], "tags": []},
    {"id": "h06", "args": [[10, 0, 10, -1]], "tags": []},
    {"id": "h07", "args": [[7, 7, 7]], "tags": []},
    {"id": "h08", "args": [[4, -4, 9, 0, 2]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
