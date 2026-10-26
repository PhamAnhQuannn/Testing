"""Hidden-test inputs for running-kth-largest; gen_hidden.py computes `expected`."""

import random

SEED = 703
BIG = 2 * 10**4


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[5], 1], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[5], 2], "tags": ["edge", "never_full"]},
        {"id": "h03", "args": [[4, 5, 8, 2], 3], "tags": []},
        {"id": "h04", "args": [[7, 7, 7, 7], 2], "tags": ["duplicates"]},
        {"id": "h05", "args": [[1, 2, 3, 4, 5], 2], "tags": ["increasing"]},
        {"id": "h06", "args": [[5, 4, 3, 2, 1], 2], "tags": ["decreasing"]},
        {"id": "h07", "args": [[0, 10**4, 0, 10**4, 3], 3], "tags": ["edge", "extremes"]},
        {"id": "h08", "args": [[rng.randint(0, 50) for _ in range(30)], 5], "tags": ["random"]},
        {
            "id": "h09",
            "args": [[rng.randint(0, 10**4) for _ in range(BIG)], 1000],
            "tags": ["stress"],
        },
        {
            "id": "h10",
            "args": [[rng.randint(0, 10**4) for _ in range(BIG)], BIG],
            "tags": ["stress"],
        },
    ]


def small_inputs(seed, n):
    """`n` argument lists: 1..12 values in 0..9 (many duplicates), k in 1..14."""
    rng = random.Random(seed)
    return [
        [[rng.randint(0, 9) for _ in range(rng.randint(1, 12))], rng.randint(1, 14)]
        for _ in range(n)
    ]
