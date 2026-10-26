"""Hidden-test inputs for height-checker; gen_hidden.py computes `expected`."""

import random

SEED = 1051


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[5]], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[1, 1, 4, 2, 1, 3]], "tags": []},
        {"id": "h03", "args": [[1, 2, 3, 4, 5]], "tags": ["sorted"]},
        {"id": "h04", "args": [[5, 4, 3, 2, 1]], "tags": ["reversed"]},
        {"id": "h05", "args": [[3, 3, 3, 3]], "tags": ["duplicates"]},
        {"id": "h06", "args": [[2, 1]], "tags": ["edge", "swap"]},
        {"id": "h07", "args": [[100, 1, 100, 1]], "tags": ["extremes"]},
        {"id": "h08", "args": [[rng.randint(1, 10) for _ in range(20)]], "tags": ["random"]},
        {"id": "h09", "args": [[rng.randint(1, 100) for _ in range(100)]], "tags": ["max"]},
        {"id": "h10", "args": [[1, 3, 2, 4, 5, 6]], "tags": []},
    ]


def small_inputs(seed, n):
    """`n` argument lists: 1..10 heights in 1..6 (many duplicates)."""
    rng = random.Random(seed)
    return [[[rng.randint(1, 6) for _ in range(rng.randint(1, 10))]] for _ in range(n)]
