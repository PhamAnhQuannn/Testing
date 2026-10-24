"""Hidden-test inputs for duplicate-zeros; tools/gen_hidden.py computes `expected`."""

import random

SEED = 1089
BIG = 10**5


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[0]], "tags": ["edge"]},
        {"id": "h02", "args": [[7]], "tags": ["edge"]},
        {"id": "h03", "args": [[1, 0]], "tags": ["edge"]},
        {"id": "h04", "args": [[0, 1]], "tags": ["edge"]},
        {"id": "h05", "args": [[1, 2, 0]], "tags": ["edge"]},
        {"id": "h06", "args": [[0, 0, 1, 0, 0]], "tags": []},
        {"id": "h07", "args": [[8, 4, 5, 0, 0, 0, 0, 7]], "tags": []},
        {
            "id": "h08",
            "args": [[rng.choice([0, 0, 1, 2, 3]) for _ in range(40)]],
            "tags": ["random"],
        },
        {"id": "h09", "args": [[rng.randint(0, 9) for _ in range(1000)]], "tags": ["random"]},
        {"id": "h10", "args": [[0] * BIG], "tags": ["stress"]},
        {"id": "h11", "args": [[rng.choice([0, 5]) for _ in range(BIG)]], "tags": ["stress"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists, each with 1-12 digits (many zeros), for the brute-force cross-check."""
    rng = random.Random(seed)
    return [[[rng.choice([0, 0, 1, 2]) for _ in range(rng.randint(1, 12))]] for _ in range(n)]
