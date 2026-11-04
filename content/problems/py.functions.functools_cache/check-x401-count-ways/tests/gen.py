"""Inputs of check-x401-count-ways.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 5], 5]},
    {"id": "s2", "args": [[2], 3]},
    {"id": "s3", "args": [[1, 2, 5], 0]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 0], "tags": ["edge"]},
    {"id": "h02", "args": [[], 5], "tags": ["edge"]},
    {"id": "h03", "args": [[3], 9], "tags": []},
    {"id": "h04", "args": [[2, 5, 3, 6], 10], "tags": []},
    {"id": "h05", "args": [[1, 2, 3], 4], "tags": []},
    {"id": "h06", "args": [[5, 10], 3], "tags": []},
    {"id": "h07", "args": [[1, 2, 5], 100], "tags": []},
    {"id": "h08", "args": [[1, 5, 10, 25, 50], 200], "tags": []},
    {"id": "h09", "args": [[7, 3, 2], 120], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
