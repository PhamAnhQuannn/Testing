"""Inputs of check-x382-build-roster.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[["bo", 95], ["an", 80], ["cu", 95]]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["solo", 90]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["a", 10], ["b", 20], ["c", 5]]], "tags": []},
    {"id": "h04", "args": [[["z", 90], ["y", 89], ["x", 91]]], "tags": []},
    {"id": "h05", "args": [[["m", 50], ["b", 50], ["k", 50]]], "tags": []},
    {"id": "h06", "args": [[["p", 100], ["q", 100], ["r", 0], ["s", 95]]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
