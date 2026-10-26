"""Hidden-test inputs for majority-element; gen_hidden.py computes `expected` from solution.py.

Every input has a majority element (count > n // 2), as the problem guarantees.
"""

import random

SEED = 169
BIG = 5 * 10**4


def _with_majority(rng, n, major, low, high):
    """`n` numbers where `major` fills strictly more than half of the positions."""
    count = n // 2 + 1
    values = [major] * count + [rng.randint(low, high) for _ in range(n - count)]
    rng.shuffle(values)
    return values


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[5]], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[3, 2, 3]], "tags": []},
        {"id": "h03", "args": [[2, 2, 1, 1, 1, 2, 2]], "tags": []},
        {"id": "h04", "args": [[-1, -1, 2, 3, -1]], "tags": ["negative"]},
        {"id": "h05", "args": [[7, 7, 7, 7]], "tags": ["all_equal"]},
        {"id": "h06", "args": [[1, 2, 3, 3, 3]], "tags": ["majority_at_end"]},
        {"id": "h07", "args": [[9, 9, 1, 2, 3, 9, 4, 9, 9]], "tags": []},
        {"id": "h08", "args": [[1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1]], "tags": ["close_margin"]},
        {"id": "h09", "args": [_with_majority(rng, 101, -(10**9), -5, 5)], "tags": ["random"]},
        {
            "id": "h10",
            "args": [_with_majority(rng, BIG, 10**9, -(10**9), 10**9)],
            "tags": ["stress"],
        },
        {"id": "h11", "args": [_with_majority(rng, BIG - 1, 0, -2, 2)], "tags": ["stress"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists with 1..11 numbers in -3..3 that always contain a majority element."""
    rng = random.Random(seed)
    return [[_with_majority(rng, rng.randint(1, 11), rng.randint(-3, 3), -3, 3)] for _ in range(n)]
