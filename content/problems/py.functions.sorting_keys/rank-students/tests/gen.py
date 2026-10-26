"""Hidden-test inputs for rank-students; gen_hidden.py computes `expected`."""

import random
import string

SEED = 2601


def _records(rng, n, max_score):
    names = set()
    while len(names) < n:
        names.add("".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(1, 6))))
    names = sorted(names)
    rng.shuffle(names)
    return [[name, rng.randint(0, max_score)] for name in names]


def hidden_inputs():
    rng = random.Random(SEED)
    return [
        {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
        {"id": "h02", "args": [[["solo", 50]]], "tags": ["edge", "single"]},
        {"id": "h03", "args": [[["an", 8], ["binh", 9], ["chi", 8]]], "tags": []},
        {"id": "h04", "args": [[["z", 5], ["a", 5]]], "tags": ["tie"]},
        {
            "id": "h05",
            "args": [[["mi", 7], ["lan", 7], ["hoa", 7], ["bao", 7]]],
            "tags": ["all_tied"],
        },
        {"id": "h06", "args": [[["b", 0], ["a", 100], ["c", 0], ["d", 100]]], "tags": ["extremes"]},
        {
            "id": "h07",
            "args": [[["ba", 3], ["bb", 2], ["a", 3], ["b", 2]]],
            "tags": ["prefix_names"],
        },
        {"id": "h08", "args": [_records(rng, 30, 5)], "tags": ["random", "many_ties"]},
        {"id": "h09", "args": [_records(rng, 200, 100)], "tags": ["random"]},
        {"id": "h10", "args": [_records(rng, 1000, 10)], "tags": ["max"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists: 0..8 distinct short names with scores in 0..3 (many ties)."""
    rng = random.Random(seed)
    return [[_records(rng, rng.randint(0, 8), 3)] for _ in range(n)]
