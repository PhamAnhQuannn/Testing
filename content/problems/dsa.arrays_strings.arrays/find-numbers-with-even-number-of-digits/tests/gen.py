"""Hidden-test inputs for find-numbers-with-even-number-of-digits."""

import random

SEED = 1295
BIG = 40_000


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[10]], "tags": ["edge"]},
        {"id": "h02", "args": [[9]], "tags": ["edge"]},
        {"id": "h03", "args": [[100000]], "tags": ["edge"]},
        {"id": "h04", "args": [[99, 100, 999, 1000, 9999, 10000, 99999]], "tags": ["edge"]},
        {"id": "h05", "args": [[1, 2, 3, 4, 5]], "tags": []},
        {"id": "h06", "args": [[11, 22, 33, 4444, 55555, 123456]], "tags": []},
        {"id": "h07", "args": [[rng.randint(1, 999999) for _ in range(50)]], "tags": ["random"]},
        {"id": "h08", "args": [[rng.randint(1, 999999) for _ in range(500)]], "tags": ["random"]},
        {"id": "h09", "args": [[rng.randint(1, 999999) for _ in range(BIG)]], "tags": ["stress"]},
        {"id": "h10", "args": [[1000] * BIG], "tags": ["stress"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists, each with 1-12 numbers of 1-6 digits, for the brute-force check."""
    rng = random.Random(seed)
    return [
        [[rng.randint(1, 10 ** rng.randint(1, 5)) for _ in range(rng.randint(1, 12))]]
        for _ in range(n)
    ]
