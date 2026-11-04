"""Inputs of check-x383-summarize-orders.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[["NEW", 10], ["PAID", 5], ["NEW", 10]]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["SHIPPED", 7]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["NEW", 1], ["NEW", 2], ["NEW", 3]]], "tags": []},
    {"id": "h04", "args": [[["PAID", 4], ["PAID", 4], ["PAID", 4]]], "tags": []},
    {"id": "h05", "args": [[["NEW", 5], ["PAID", 5], ["SHIPPED", 5]]], "tags": []},
    {"id": "h06", "args": [[["SHIPPED", 0], ["NEW", 0], ["SHIPPED", 0], ["PAID", 9]]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
