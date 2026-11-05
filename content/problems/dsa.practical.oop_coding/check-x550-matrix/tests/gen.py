"""Inputs of check-x550-matrix.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Matrix", "set", "transpose", "dims", "get"],
    "args": [[2, 3], [0, 2, 7], [], [], [2, 0]],
}

HIDDEN = [
    {"id": "h01", "ops": ["Matrix", "dims", "get"], "args": [[2, 2], [], [1, 1]], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["Matrix", "set", "set", "get", "get", "dims"],
        "args": [[3, 3], [0, 0, 5], [2, 1, -4], [0, 0], [2, 1], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Matrix", "transpose", "dims"],
        "args": [[2, 5], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["Matrix", "set", "set", "transpose", "get", "get", "get", "dims"],
        "args": [[2, 3], [0, 1, 9], [1, 2, 4], [], [1, 0], [2, 1], [0, 1], []],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["Matrix", "set", "set", "get"],
        "args": [[1, 1], [0, 0, 1], [0, 0, 8], [0, 0]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["Matrix", "set", "transpose", "transpose", "get", "dims"],
        "args": [[2, 3], [1, 2, 6], [], [], [1, 2], []],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Matrix", "transpose", "set", "get", "dims"],
        "args": [[1, 4], [], [3, 0, 2], [3, 0], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
