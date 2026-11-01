"""Hidden-test inputs for fix-two-sum; expected comes from solution.py."""

import random


def hidden_inputs():
    rng = random.Random(1)
    big = rng.sample(range(-(10**6), 10**6), 2000)
    return [
        {"id": "h01", "args": [[2, 7, 11, 15], 9], "tags": []},
        {"id": "h02", "args": [[3, 2, 4], 6], "tags": ["edge", "self-pair"]},
        {"id": "h03", "args": [[3, 3], 6], "tags": ["duplicate"]},
        {"id": "h04", "args": [[5], 10], "tags": ["self-pair", "none"]},
        {"id": "h05", "args": [[1, 2, 3], 100], "tags": ["none"]},
        {"id": "h06", "args": [[-1, -2, -3, -4], -6], "tags": []},
        {"id": "h07", "args": [[0, 4, 3, 0], 0], "tags": ["duplicate"]},
        {"id": "h08", "args": [[4, 1, 8, 5], 8], "tags": ["edge", "self-pair"]},
        {"id": "h09", "args": [big, big[3] + big[1900]], "tags": ["stress"]},
        {"id": "h10", "args": [[], 5], "tags": ["empty"]},
    ]


def small_inputs(seed, n):
    return []
