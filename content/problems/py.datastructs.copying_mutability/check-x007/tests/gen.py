"""Hidden-test inputs for check-x007; tools/gen_hidden.py computes `expected` from solution.py."""

import random


def hidden_inputs():
    rng = random.Random(7)
    big = [[rng.randint(-100, 100) for _ in range(rng.randint(0, 6))] for _ in range(20)]
    return [
        {"id": "h01", "args": [[[1]]], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[]], "tags": ["edge", "empty"]},
        {"id": "h03", "args": [[[1, 2], [3, 4]]], "tags": []},
        {"id": "h04", "args": [[[0, 0], [0, 0], [0, 0]]], "tags": ["zeros"]},
        {"id": "h05", "args": [[[-1, -2, -3]]], "tags": ["negative"]},
        {"id": "h06", "args": [[[5], [], [7, 8, 9]]], "tags": ["ragged", "empty_row"]},
        {"id": "h07", "args": [[[9, 9], [9, 9]]], "tags": []},
        {"id": "h08", "args": [big], "tags": ["random"]},
    ]


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
