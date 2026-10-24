"""Hidden-test inputs for max-consecutive-ones; tools/gen_hidden.py computes `expected`."""

import random

SEED = 485
BIG = 10**5


def hidden_inputs():
    rng = random.Random(SEED)
    middle_run = [0] * 30_000 + [1] * 40_000 + [0] * 30_000
    return [
        {"id": "h01", "args": [[1]], "tags": ["edge"]},
        {"id": "h02", "args": [[0, 0, 0]], "tags": ["edge"]},
        {"id": "h03", "args": [[1, 1, 1, 1]], "tags": ["edge"]},
        {"id": "h04", "args": [[0, 1, 1, 1]], "tags": ["edge"]},
        {"id": "h05", "args": [[1, 0, 1, 1]], "tags": []},
        {"id": "h06", "args": [[1, 1, 0, 1]], "tags": []},
        {"id": "h07", "args": [[1, 0, 1, 0, 1, 0, 1]], "tags": []},
        {"id": "h08", "args": [[1, 1, 0, 0, 1, 1, 1, 0, 1]], "tags": []},
        {"id": "h09", "args": [[rng.randint(0, 1) for _ in range(30)]], "tags": ["random"]},
        {"id": "h10", "args": [[rng.randint(0, 1) for _ in range(1000)]], "tags": ["random"]},
        {"id": "h11", "args": [[1] * BIG], "tags": ["stress"]},
        {"id": "h12", "args": [middle_run], "tags": ["stress"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists, each with 1-12 bits, for the brute-force cross-check."""
    rng = random.Random(seed)
    return [[[rng.randint(0, 1) for _ in range(rng.randint(1, 12))]] for _ in range(n)]
