"""Hidden-test inputs for compute-prf; expected comes from solution.py."""

import random


def hidden_inputs():
    return [
        {"id": "h01", "args": [[], []], "tags": ["empty"]},
        {"id": "h02", "args": [[0, 0, 0], [0, 0, 0]], "tags": ["edge"]},
        {"id": "h03", "args": [[0, 0, 0], [1, 1, 0]], "tags": ["edge"]},
        {"id": "h04", "args": [[1, 1, 0], [0, 0, 0]], "tags": ["edge"]},
        {"id": "h05", "args": [[1, 1, 1], [1, 1, 1]], "tags": ["edge"]},
        {"id": "h06", "args": [[1, 0, 1, 0], [0, 1, 0, 1]], "tags": ["edge"]},
        {"id": "h07", "args": [[1, 0, 1, 1, 0, 0, 1], [1, 1, 0, 1, 0, 0, 0]], "tags": []},
        {"id": "h08", "args": [[1, 1, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]], "tags": []},
        {"id": "h09", "args": [[1], [0]], "tags": ["edge"]},
        {"id": "h10", "args": [[0, 1, 1, 0, 1, 0, 1, 1], [0, 1, 0, 0, 1, 1, 1, 1]], "tags": []},
    ]


def small_inputs(seed, n):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        size = rng.randint(0, 12)
        out.append(
            {
                "id": f"r{i:02d}",
                "args": [
                    [rng.randint(0, 1) for _ in range(size)],
                    [rng.randint(0, 1) for _ in range(size)],
                ],
                "tags": [],
            }
        )
    return out
