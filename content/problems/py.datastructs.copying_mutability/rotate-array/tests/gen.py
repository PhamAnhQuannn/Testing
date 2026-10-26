"""Hidden-test inputs for rotate-array; gen_hidden.py computes `expected` from solution.py."""

import random

SEED = 189
BIG = 5 * 10**4


def hidden_inputs():
    rng = random.Random(SEED)
    small = [rng.randint(-50, 50) for _ in range(9)]
    big = [rng.randint(-99, 99) for _ in range(BIG)]
    return [
        {"id": "h01", "args": [[1], 0], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[1], 5], "tags": ["edge", "single"]},
        {"id": "h03", "args": [[1, 2, 3, 4, 5], 0], "tags": ["edge", "k_zero"]},
        {"id": "h04", "args": [[1, 2, 3, 4, 5], 5], "tags": ["edge", "k_equals_n"]},
        {"id": "h05", "args": [[1, 2, 3, 4, 5, 6, 7], 3], "tags": []},
        {"id": "h06", "args": [[-1, -100, 3, 99], 2], "tags": []},
        {"id": "h07", "args": [[1, 2, 3], 4], "tags": ["edge", "k_gt_n"]},
        {"id": "h08", "args": [[1, 2], 3], "tags": ["edge", "k_gt_n"]},
        {"id": "h09", "args": [small, 23], "tags": ["random", "k_gt_n"]},
        {"id": "h10", "args": [big, 99999], "tags": ["stress", "max"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists: 1..12 elements, k in 0..40 (often larger than the length)."""
    rng = random.Random(seed)
    cases = []
    for _ in range(n):
        size = rng.randint(1, 12)
        cases.append([[rng.randint(-9, 9) for _ in range(size)], rng.randint(0, 40)])
    return cases
