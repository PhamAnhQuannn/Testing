"""Hidden-test inputs for flipping-an-image; gen_hidden.py computes `expected` from solution.py."""

import random

SEED = 832


def _square(rng, n):
    return [[rng.randint(0, 1) for _ in range(n)] for _ in range(n)]


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[[0]]], "tags": ["edge", "n1"]},
        {"id": "h02", "args": [[[1]]], "tags": ["edge", "n1"]},
        {"id": "h03", "args": [[[1, 0], [0, 1]]], "tags": ["edge"]},
        {"id": "h04", "args": [[[1, 1, 1], [1, 1, 1], [1, 1, 1]]], "tags": ["all_ones"]},
        {"id": "h05", "args": [[[0, 0, 0], [0, 0, 0], [0, 0, 0]]], "tags": ["all_zeros"]},
        {"id": "h06", "args": [[[1, 0, 1], [0, 1, 0], [1, 1, 0]]], "tags": ["palindrome_rows"]},
        {
            "id": "h07",
            "args": [[[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]]],
            "tags": [],
        },
        {"id": "h08", "args": [_square(rng, 5)], "tags": ["random"]},
        {"id": "h09", "args": [_square(rng, 10)], "tags": ["random"]},
        {"id": "h10", "args": [_square(rng, 20)], "tags": ["random", "max"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists, each a random square image with side 1..6."""
    rng = random.Random(seed)
    return [[_square(rng, rng.randint(1, 6))] for _ in range(n)]
