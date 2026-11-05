"""Inputs of check-x522-top-spenders.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Ledger", "open", "open", "open", "pay", "transfer", "pay", "top_spenders"],
    "args": [[], ["a"], ["b"], ["c"], ["a", 100], ["b", "c", 100], ["c", 50], [2]],
}

HIDDEN = [
    {"id": "h01", "ops": ["Ledger", "top_spenders"], "args": [[], [3]], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["Ledger", "open", "open", "pay", "top_spenders"],
        "args": [[], ["b"], ["a"], ["a", 5], [10]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["Ledger", "open", "open", "open", "top_spenders", "top_spenders"],
        "args": [[], ["z"], ["m"], ["a"], [2], [3]],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["Ledger", "open", "open", "pay", "pay", "top_spenders", "top_spenders"],
        "args": [[], ["x"], ["y"], ["x", 300], ["y", 301], [1], [2]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["Ledger", "open", "transfer", "transfer", "pay", "top_spenders"],
        "args": [[], ["a"], ["a", "ghost", 10], ["ghost", "a", 10], ["ghost", 5], [5]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": [
            "Ledger",
            "open",
            "open",
            "open",
            "open",
            "pay",
            "pay",
            "transfer",
            "transfer",
            "pay",
            "top_spenders",
            "top_spenders",
        ],
        "args": [
            [],
            ["d"],
            ["c"],
            ["b"],
            ["a"],
            ["a", 200],
            ["d", 100],
            ["c", "a", 100],
            ["b", "a", 200],
            ["d", 100],
            [3],
            [4],
        ],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Ledger", "open", "open", "pay", "pay", "transfer", "top_spenders", "top_spenders"],
        "args": [[], ["a"], ["b"], ["a", 0], ["b", -3], ["a", "b", 0], [2], [0]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
