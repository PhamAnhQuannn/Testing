import random


def hidden_inputs():
    rng = random.Random(7)
    rows = [
        {"id": "h01", "args": [[]], "tags": ["edge"]},
        {"id": "h02", "args": [[0]], "tags": ["edge"]},
        {"id": "h03", "args": [[1]], "tags": []},
        {"id": "h04", "args": [[2, 4, 6]], "tags": []},
        {"id": "h05", "args": [[1, 3, 5]], "tags": []},
        {"id": "h06", "args": [[1, 2, 3, 4, 5, 6]], "tags": []},
        {"id": "h07", "args": [[-2, -1, 0]], "tags": []},
        {"id": "h08", "args": [[rng.randint(0, 99) for _ in range(30)]], "tags": ["random"]},
        {"id": "h09", "args": [[rng.randint(0, 99) for _ in range(20000)]], "tags": ["stress"]},
    ]
    return rows


def small_inputs(seed, n):
    rng = random.Random(seed)
    return [[[rng.randint(0, 9) for _ in range(rng.randint(0, 12))]] for _ in range(n)]
