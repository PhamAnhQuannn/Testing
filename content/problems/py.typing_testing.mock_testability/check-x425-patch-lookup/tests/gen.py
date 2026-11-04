"""Inputs of check-x425-patch-lookup.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[1, 2]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [[7]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[0]], "tags": ["edge"]},
    {"id": "h03", "args": [[5]], "tags": []},
    {"id": "h04", "args": [[1, 2, 3]], "tags": []},
    {"id": "h05", "args": [[3, 3, 3]], "tags": []},
    {"id": "h06", "args": [[10, 20, 30, 40]], "tags": []},
    {"id": "h07", "args": [[-1, 0, 1]], "tags": []},
    {"id": "h08", "args": [[9, 8, 7, 6, 5, 4]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
