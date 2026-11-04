"""Inputs of check-x386-price-lookup.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[[5, "USD", "a"]], [[5, "USD"], [6, "USD"]]]}

HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge"]},
    {"id": "h02", "args": [[], [[1, "USD"]]], "tags": ["edge"]},
    {
        "id": "h03",
        "args": [[[5, "USD", "a"], [5, "EUR", "b"]], [[5, "EUR"], [5, "USD"]]],
        "tags": [],
    },
    {"id": "h04", "args": [[[5, "USD", "a"], [5, "USD", "z"]], [[5, "USD"]]], "tags": []},
    {
        "id": "h05",
        "args": [[[1, "VND", "x"], [2, "VND", "y"]], [[2, "VND"], [3, "VND"], [1, "usd"]]],
        "tags": [],
    },
    {"id": "h06", "args": [[[0, "A", "zero"]], [[0, "A"], [0, "A"]]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
