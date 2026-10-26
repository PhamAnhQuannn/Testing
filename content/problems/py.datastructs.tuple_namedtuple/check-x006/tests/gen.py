"""Hidden-test inputs for check-x006; tools/gen_hidden.py computes `expected` from solution.py."""

import random


def hidden_inputs():
    rng = random.Random(6)
    names = ["An", "Binh", "Chi", "Dung", "Em", "Phuc", "Giang", "Hoa"]
    big = [[rng.choice(names), rng.randint(-1000, 1000)] for _ in range(1000)]
    return [
        {"id": "h01", "args": [[["An", 5]]], "tags": ["edge", "single"]},
        {"id": "h02", "args": [[["An", 7], ["Binh", 9], ["Chi", 9]]], "tags": ["tie"]},
        {"id": "h03", "args": [[["An", 9], ["Binh", 9], ["Chi", 9]]], "tags": ["tie", "all_equal"]},
        {"id": "h04", "args": [[["An", -3], ["Binh", -8], ["Chi", -5]]], "tags": ["negative"]},
        {"id": "h05", "args": [[["An", 1], ["Binh", 2], ["Chi", 3]]], "tags": ["last_wins"]},
        {"id": "h06", "args": [[["An", 3], ["Binh", 2], ["Chi", 1]]], "tags": ["first_wins"]},
        {
            "id": "h07",
            "args": [[["Dung", 0], ["Em", 10], ["Phuc", 4], ["Giang", 10]]],
            "tags": ["tie"],
        },
        {"id": "h08", "args": [[["An", 1000], ["Binh", -1000]]], "tags": ["edge", "extremes"]},
        {"id": "h09", "args": [big], "tags": ["random", "max"]},
    ]


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
