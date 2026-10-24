import random


def hidden_inputs():
    values = [0, 1, -1, 5, 100, 7, 12]
    return [
        {"id": f"h{i:02d}", "args": [v], "tags": ["edge"] if v == 0 else []}
        for i, v in enumerate(values, start=1)
    ]


def small_inputs(seed, n):
    rng = random.Random(seed)
    return [[rng.randint(-9, 9)] for _ in range(n)]
