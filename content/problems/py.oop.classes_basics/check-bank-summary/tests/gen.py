"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[["a", "deposit", 100], ["a", "withdraw", 30]]]},
    {"id": "s2", "args": [[["a", "withdraw", 10]]]},
    {
        "id": "s3",
        "args": [
            [
                ["b", "deposit", 50],
                ["a", "deposit", 20],
                ["b", "withdraw", 30],
                ["a", "withdraw", 25],
            ]
        ],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["a", "deposit", 100]]], "tags": []},
    {"id": "h03", "args": [[["a", "withdraw", 10]]], "tags": []},
    {
        "id": "h04",
        "args": [[["a", "deposit", 100], ["a", "withdraw", 100], ["a", "withdraw", 1]]],
        "tags": [],
    },
    {
        "id": "h05",
        "args": [
            [
                ["b", "deposit", 50],
                ["a", "deposit", 20],
                ["b", "withdraw", 30],
                ["a", "withdraw", 25],
            ]
        ],
        "tags": [],
    },
    {
        "id": "h06",
        "args": [[["a", "deposit", 0], ["a", "deposit", -5], ["a", "withdraw", 0]]],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [[["z", "deposit", 5], ["m", "deposit", 7], ["a", "deposit", 9]]],
        "tags": [],
    },
    {
        "id": "h08",
        "args": [
            [
                ["x", "deposit", 10],
                ["x", "deposit", 10],
                ["x", "withdraw", 5],
                ["x", "withdraw", 50],
                ["x", "deposit", 1],
            ]
        ],
        "tags": [],
    },
    {
        "id": "h09",
        "args": [
            [
                ["c", "deposit", 1000],
                ["d", "withdraw", 1],
                ["c", "withdraw", 999],
                ["d", "deposit", 3],
                ["c", "withdraw", 2],
            ]
        ],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
