"""Inputs of check-x424-mock-fallback.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[5, None, 7]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [[None, None]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[None]], "tags": ["edge"]},
    {"id": "h03", "args": [[9]], "tags": []},
    {"id": "h04", "args": [[1, 2, 3, 4]], "tags": []},
    {"id": "h05", "args": [[None, 4, None, 8]], "tags": []},
    {"id": "h06", "args": [[None, None, None]], "tags": []},
    {"id": "h07", "args": [[0, None, 0]], "tags": []},
    {"id": "h08", "args": [[10, 20, None, 40, 50, None, 70]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
