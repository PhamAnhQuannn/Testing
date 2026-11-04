"""Inputs of check-x373: stats summary via statistics.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[1, 2, 2, 3, 4]]}

HIDDEN = [
    {"id": "h01", "args": [[5]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3, 4]], "tags": []},
    {"id": "h03", "args": [[2, 2, 3, 3, 3]], "tags": []},
    {"id": "h04", "args": [[10, 20, 30, 20]], "tags": []},
    {"id": "h05", "args": [[7, 7, 7]], "tags": []},
    {"id": "h06", "args": [[1, 2, 2, 5, 9, 9, 9]], "tags": []},
    {"id": "h07", "args": [[-3, -1, -1, 4]], "tags": []},
    {"id": "h08", "args": [[1, 1, 2]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
