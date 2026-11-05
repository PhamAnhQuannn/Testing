"""Inputs of check-x518-ttl-store (class_ops, injectable clock `now`).

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["TTLStore", "set", "get", "get", "get"],
    "args": [[], ["a", 1, 0, 5], ["a", 4], ["a", 5], ["a", 6]],
}

HIDDEN = [
    {"id": "h01", "ops": ["TTLStore", "get"], "args": [[], ["x", 0]], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["TTLStore", "set", "get", "get"],
        "args": [[], ["k", "v", 10, 3], ["k", 12], ["k", 13]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["TTLStore", "set", "set", "get", "get"],
        "args": [[], ["a", 1, 0, 2], ["a", 2, 1, 10], ["a", 5], ["a", 11]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["TTLStore", "set", "delete", "get", "delete"],
        "args": [[], ["a", 1, 0, 9], ["a"], ["a", 1], ["a"]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["TTLStore", "set", "set", "get", "get", "get"],
        "args": [[], ["a", 1, 0, 3], ["b", 2, 0, 6], ["a", 3], ["b", 3], ["b", 6]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["TTLStore", "set", "get", "set", "get"],
        "args": [[], ["a", 0, 0, 1], ["a", 1], ["a", 7, 1, 1], ["a", 1]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["TTLStore", "set", "get", "get"],
        "args": [[], ["z", None, 5, 5], ["z", 9], ["z", 10]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
