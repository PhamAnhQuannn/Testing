"""Inputs of check-x556-safe-counter.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["SafeCounter", "incr", "incr", "add", "value"],
    "args": [[], [], [], [5], []],
}

HIDDEN = [
    {"id": "h01", "ops": ["SafeCounter", "value"], "args": [[], []], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["SafeCounter", "incr", "incr", "incr", "value"],
        "args": [[], [], [], [], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["SafeCounter", "add", "add", "value"],
        "args": [[], [4], [6], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["SafeCounter", "add", "value", "incr", "value", "add", "value"],
        "args": [[], [100], [], [], [], [0], []],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["SafeCounter", "add", "incr", "add", "value"],
        "args": [[], [-3], [], [10], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["SafeCounter"] + ["incr"] * 50 + ["value"],
        "args": [[]] + [[]] * 50 + [[]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
