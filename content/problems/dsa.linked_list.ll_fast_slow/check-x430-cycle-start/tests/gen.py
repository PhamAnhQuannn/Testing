"""Inputs of check-x430-cycle-start.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[3, 2, 0, -4], 1]}

HIDDEN = [
    {"id": "h01", "args": [[1, 2, 3, 4, 5], 2], "tags": []},
    {"id": "h02", "args": [[1, 2, 3, 4, 5], -1], "tags": []},
    {"id": "h03", "args": [[], -1], "tags": ["edge"]},
    {"id": "h04", "args": [[7], 0], "tags": ["edge"]},
    {"id": "h05", "args": [[7], -1], "tags": ["edge"]},
    {"id": "h06", "args": [[1, 2], 0], "tags": ["edge"]},
    {"id": "h07", "args": [[1, 2], -1], "tags": []},
    {"id": "h08", "args": [[1, 2, 3, 4], 0], "tags": []},
    {"id": "h09", "args": [[1, 2, 3, 4], 3], "tags": []},
    {"id": "h10", "args": [[5, 6, 7, 8, 9, 10], 4], "tags": []},
    {"id": "h11", "args": [[5, 5, 5, 5], 1], "tags": []},
    {"id": "h12", "args": [[0, -1, -2, -3, -4, -5, -6], 2], "tags": []},
    {"id": "h13", "args": [[1, 2, 3], 1], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
