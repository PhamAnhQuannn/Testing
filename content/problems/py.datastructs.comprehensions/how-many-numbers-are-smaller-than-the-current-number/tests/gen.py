"""Hidden-test inputs for how-many-numbers-are-smaller-than-the-current-number; tools/gen_hidden.py
computes `expected` from solution.py."""

import random

SEED = 1365


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[0, 0]], "tags": ["edge", "min_len"]},
        {"id": "h02", "args": [[5, 3]], "tags": ["edge", "min_len"]},
        {"id": "h03", "args": [[7, 7, 7, 7]], "tags": ["all_equal"]},
        {"id": "h04", "args": [[1, 2, 3, 4, 5]], "tags": ["sorted"]},
        {"id": "h05", "args": [[5, 4, 3, 2, 1]], "tags": ["descending"]},
        {"id": "h06", "args": [[8, 1, 2, 2, 3]], "tags": ["duplicates"]},
        {"id": "h07", "args": [[100, 0, 100, 0, 50]], "tags": ["extremes"]},
        {"id": "h08", "args": [[rng.randint(0, 100) for _ in range(30)]], "tags": ["random"]},
        {"id": "h09", "args": [[rng.randint(0, 5) for _ in range(60)]], "tags": ["many_dups"]},
        {"id": "h10", "args": [[rng.randint(0, 100) for _ in range(500)]], "tags": ["max"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists with 2..10 numbers in 0..8 (many duplicates) for the brute cross-check."""
    rng = random.Random(seed)
    return [[[rng.randint(0, 8) for _ in range(rng.randint(2, 10))]] for _ in range(n)]
