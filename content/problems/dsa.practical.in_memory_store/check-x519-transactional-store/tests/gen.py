"""Inputs of check-x519-transactional-store (class_ops, nested transactions).

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["TxnStore", "set", "begin", "set", "get", "rollback", "get", "commit"],
    "args": [[], ["a", 1], [], ["a", 2], ["a"], [], ["a"], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["TxnStore", "get", "commit", "rollback"],
        "args": [[], ["x"], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["TxnStore", "begin", "set", "get", "commit", "get"],
        "args": [[], [], ["a", 1], ["a"], [], ["a"]],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["TxnStore", "begin", "set", "rollback", "get"],
        "args": [[], [], ["a", 1], [], ["a"]],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": [
            "TxnStore",
            "set",
            "begin",
            "set",
            "begin",
            "set",
            "get",
            "rollback",
            "get",
            "rollback",
            "get",
        ],
        "args": [[], ["a", 1], [], ["a", 2], [], ["a", 3], ["a"], [], ["a"], [], ["a"]],
        "tags": ["nested"],
    },
    {
        "id": "h05",
        "ops": [
            "TxnStore",
            "set",
            "begin",
            "begin",
            "set",
            "commit",
            "get",
            "rollback",
            "get",
            "rollback",
        ],
        "args": [[], ["a", 1], [], [], ["a", 5], [], ["a"], [], ["a"], []],
        "tags": ["nested", "edge"],
    },
    {
        "id": "h06",
        "ops": [
            "TxnStore",
            "begin",
            "set",
            "begin",
            "set",
            "set",
            "commit",
            "rollback",
            "get",
            "get",
        ],
        "args": [[], [], ["a", 1], [], ["b", 2], ["a", 9], [], [], ["a"], ["b"]],
        "tags": ["nested"],
    },
    {
        "id": "h07",
        "ops": [
            "TxnStore",
            "begin",
            "set",
            "begin",
            "set",
            "commit",
            "commit",
            "get",
            "commit",
            "rollback",
        ],
        "args": [[], [], ["k", "x"], [], ["k", "y"], [], [], ["k"], [], []],
        "tags": ["nested", "edge"],
    },
    {
        "id": "h08",
        "ops": ["TxnStore", "set", "set", "begin", "set", "rollback", "get", "get", "rollback"],
        "args": [[], ["a", 1], ["b", 2], [], ["a", 7], [], ["a"], ["b"], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
