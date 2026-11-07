"""Inputs of check-x790-apply-ops; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [
            [["insert", "an", 5], ["insert", "binh", 3], ["update", "an", 9], ["delete", "binh"]]
        ],
    },
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {
        "id": "h02",
        "args": [[["insert", "a", 1], ["insert", "b", 2], ["delete", "a"], ["delete", "b"]]],
        "tags": ["edge"],
    },
    {"id": "h03", "args": [[["update", "ghost", 7]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["delete", "ghost"], ["insert", "x", 1]]], "tags": ["edge"]},
    {
        "id": "h05",
        "args": [[["insert", "a", 1], ["insert", "a", 2], ["insert", "a", 3]]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "args": [
            [
                ["insert", "m", 4],
                ["update", "m", 5],
                ["insert", "k", 1],
                ["delete", "m"],
                ["insert", "m", 8],
                ["update", "k", -2],
            ]
        ],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [[["insert", "o'brien", 3], ["insert", "a;b", 4], ["update", "o'brien", 6]]],
        "tags": ["edge"],
    },
    {
        "id": "h08",
        "args": [[["insert", "neg", -5], ["insert", "zero", 0], ["update", "zero", -1]]],
        "tags": ["edge"],
    },
    {
        "id": "h09",
        "args": [[["insert", "b", 2], ["insert", "a", 1], ["insert", "c", 3]]],
        "tags": ["edge"],
    },
    {
        "id": "h10",
        "args": [[["insert", "a", 1], ["delete", "a"], ["update", "a", 9], ["insert", "a", 2]]],
        "tags": ["edge"],
    },
]

_POOL = ["apple", "banana", "cherry", "date", "elder"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_ops = (x >> 8) % 14
        ops = []
        for _r in range(n_ops):
            x = (x * 1103515245 + 12345) % 2147483648
            kind = (x >> 8) % 3
            x = (x * 1103515245 + 12345) % 2147483648
            name = _POOL[(x >> 8) % len(_POOL)]
            x = (x * 1103515245 + 12345) % 2147483648
            score = (x >> 8) % 11 - 5
            if kind == 0:
                ops.append(["insert", name, score])
            elif kind == 1:
                ops.append(["update", name, score])
            else:
                ops.append(["delete", name])
        out.append([ops])
    return out


for _i, _a in enumerate(_lcg(31, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
