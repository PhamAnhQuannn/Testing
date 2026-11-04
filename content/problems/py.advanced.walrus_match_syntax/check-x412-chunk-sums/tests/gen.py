"""Inputs of check-x412-chunk-sums.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4, 5], 2]},
    {"id": "s2", "args": [[], 3]},
    {"id": "s3", "args": [[4, 4, 4], 3]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 1], "tags": ["edge"]},
    {"id": "h02", "args": [[7], 1], "tags": ["edge"]},
    {"id": "h03", "args": [[7], 5], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 3, 4, 5, 6], 2], "tags": []},
    {"id": "h05", "args": [[1, 2, 3, 4, 5, 6, 7], 3], "tags": []},
    {"id": "h06", "args": [[-1, -2, 3, 4], 2], "tags": []},
    {"id": "h07", "args": [[0, 0, 0, 0], 4], "tags": []},
    {"id": "h08", "args": [[5, 10, 15], 1], "tags": []},
    {"id": "h09", "args": [list(range(1, 21)), 6], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
