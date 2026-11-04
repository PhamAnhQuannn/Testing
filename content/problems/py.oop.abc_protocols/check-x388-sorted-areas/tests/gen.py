"""Inputs of check-x388-sorted-areas.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[["sq", 3], ["rect", 2, 5], ["tri", 4, 3]]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["sq", 1]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["tri", 3, 3]]], "tags": []},
    {"id": "h04", "args": [[["rect", 4, 6], ["sq", 2], ["tri", 10, 10]]], "tags": []},
    {"id": "h05", "args": [[["sq", 5], ["sq", 5], ["rect", 5, 5]]], "tags": []},
    {"id": "h06", "args": [[["tri", 1, 1], ["rect", 1, 1], ["sq", 0]]], "tags": []},
    {"id": "h07", "args": [[["rect", 7, 3], ["sq", 4], ["tri", 5, 5], ["sq", 3]]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
