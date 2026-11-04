"""Inputs of check-x407-lookup-order.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [[["d", "x"], ["n", "y"]]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [[["n", "a"], ["n", "b"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["d", "x"]]], "tags": []},
    {"id": "h03", "args": [[["n", "y"]]], "tags": []},
    {"id": "h04", "args": [[["d", "1"], ["d", "2"]]], "tags": []},
    {"id": "h05", "args": [[["n", "a"], ["d", "b"], ["n", "c"]]], "tags": []},
    {"id": "h06", "args": [[["d", "x"], ["n", "y"], ["d", "z"]]], "tags": []},
    {"id": "h07", "args": [[["n", ""], ["d", ""]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["d", 5], ["n", 6]]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
