"""Hidden-test inputs for concatenation-of-array; tools/gen_hidden.py computes `expected`."""

import random

SEED = 1929
BIG = 30_000


def hidden_inputs():
    rng = random.Random(SEED)

    def numbers(n, high=1000):
        return [rng.randint(1, high) for _ in range(n)]

    return [
        {"id": "h01", "args": [[5]], "tags": ["edge"]},
        {"id": "h02", "args": [[1, 2]], "tags": ["edge"]},
        {"id": "h03", "args": [[4, 4, 4]], "tags": []},
        {"id": "h04", "args": [[1000, 1, 1000]], "tags": []},
        {"id": "h05", "args": [[3, 1, 2, 3, 1, 2]], "tags": []},
        {"id": "h06", "args": [numbers(10)], "tags": ["random"]},
        {"id": "h07", "args": [numbers(100)], "tags": ["random"]},
        {"id": "h08", "args": [numbers(1000)], "tags": ["random"]},
        {"id": "h09", "args": [numbers(BIG)], "tags": ["stress"]},
        {"id": "h10", "args": [[7] * BIG], "tags": ["stress"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists, each with 1-12 numbers, for the brute-force cross-check."""
    rng = random.Random(seed)
    return [[[rng.randint(1, 9) for _ in range(rng.randint(1, 12))]] for _ in range(n)]
