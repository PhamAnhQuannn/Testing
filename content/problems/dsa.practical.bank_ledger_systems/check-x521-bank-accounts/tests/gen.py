"""Inputs of check-x521-bank-accounts.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Bank", "open", "open", "deposit", "transfer", "withdraw", "balance", "balance"],
    "args": [[], ["a"], ["b"], ["a", 500], ["a", "b", 200], ["b", 300], ["a"], ["b"]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Bank", "balance", "deposit", "withdraw", "transfer"],
        "args": [[], ["x"], ["x", 10], ["x", 10], ["x", "y", 1]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["Bank", "open", "deposit", "withdraw", "withdraw", "balance"],
        "args": [[], ["a"], ["a", 1000], ["a", 1001], ["a", 1000], ["a"]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["Bank", "open", "open", "deposit", "transfer", "transfer", "balance", "balance"],
        "args": [[], ["a"], ["b"], ["a", 100], ["a", "b", 101], ["a", "b", 100], ["a"], ["b"]],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["Bank", "open", "deposit", "transfer", "transfer", "balance"],
        "args": [[], ["a"], ["a", 50], ["a", "ghost", 10], ["ghost", "a", 10], ["a"]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["Bank", "open", "deposit", "deposit", "withdraw", "balance", "open", "balance"],
        "args": [[], ["a"], ["a", 0], ["a", -5], ["a", 0], ["a"], ["a"], ["a"]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": [
            "Bank",
            "open",
            "open",
            "open",
            "deposit",
            "transfer",
            "transfer",
            "transfer",
            "balance",
            "balance",
            "balance",
        ],
        "args": [
            [],
            ["a"],
            ["b"],
            ["c"],
            ["a", 999],
            ["a", "b", 333],
            ["b", "c", 100],
            ["c", "a", 100],
            ["a"],
            ["b"],
            ["c"],
        ],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Bank", "open", "deposit", "transfer", "balance"],
        "args": [[], ["a"], ["a", 70], ["a", "a", 30], ["a"]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
