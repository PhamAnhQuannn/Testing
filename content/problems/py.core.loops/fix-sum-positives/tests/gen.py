"""Hidden-test inputs for fix-sum-positives; expected comes from solution.py."""

import random


def hidden_inputs():
    rng = random.Random(7)
    return [
        {"id": "h01", "args": [[]], "tags": ["empty"]},
        {"id": "h02", "args": [[1, 2, 3]], "tags": []},
        {"id": "h03", "args": [[-1, 2, 3]], "tags": ["edge"]},
        {"id": "h04", "args": [[1, -2, 3]], "tags": ["edge"]},
        {"id": "h05", "args": [[1, 2, -3]], "tags": []},
        {"id": "h06", "args": [[-1, -2, -3]], "tags": []},
        {"id": "h07", "args": [[0, 5, 0, 5]], "tags": ["zero"]},
        {"id": "h08", "args": [[rng.randint(-50, 50) for _ in range(200)]], "tags": ["random"]},
    ]


def small_inputs(seed, n):
    return []
