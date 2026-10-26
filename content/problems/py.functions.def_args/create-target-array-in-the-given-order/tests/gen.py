"""Hidden inputs for create-target-array-in-the-given-order; gen_hidden.py computes `expected`."""

import random

SEED = 1389


def _pair(rng, n):
    return [[rng.randint(0, 100) for _ in range(n)], [rng.randint(0, i) for i in range(n)]]


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[7], [0]], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[0, 1, 2, 3, 4], [0, 1, 2, 2, 1]], "tags": []},
        {"id": "h03", "args": [[1, 2, 3, 4, 0], [0, 1, 2, 3, 0]], "tags": []},
        {"id": "h04", "args": [[1, 2, 3, 4], [0, 1, 2, 3]], "tags": ["append_only"]},
        {"id": "h05", "args": [[1, 2, 3, 4], [0, 0, 0, 0]], "tags": ["always_front"]},
        {"id": "h06", "args": [[5, 5, 5], [0, 1, 1]], "tags": ["duplicates"]},
        {"id": "h07", "args": [[100, 0], [0, 0]], "tags": ["edge", "extremes"]},
        {"id": "h08", "args": _pair(rng, 12), "tags": ["random"]},
        {"id": "h09", "args": _pair(rng, 40), "tags": ["random"]},
        {"id": "h10", "args": _pair(rng, 100), "tags": ["max"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists: 1..8 values with valid insertion positions."""
    rng = random.Random(seed)
    return [_pair(rng, rng.randint(1, 8)) for _ in range(n)]
