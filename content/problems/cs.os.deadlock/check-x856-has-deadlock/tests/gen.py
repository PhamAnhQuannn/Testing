"""Inputs of check-x856-has-deadlock; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 2], [2, 3], [3, 1]]]},
    {"id": "s2", "args": [[[1, 2], [2, 3]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[[5, 5]]], "tags": ["edge", "self-loop"]},
    {"id": "h03", "args": [[[1, 2]]], "tags": ["edge", "single-edge"]},
    {
        "id": "h04",
        "args": [[[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]],
        "tags": ["long-chain", "acyclic"],
    },
    {"id": "h05", "args": [[[1, 2], [2, 1]]], "tags": ["two-cycle"]},
    {
        "id": "h06",
        "args": [[[1, 2], [2, 3], [3, 4], [4, 2], [5, 1]]],
        "tags": ["cycle-not-all-nodes"],
    },
    {
        "id": "h07",
        "args": [[[1, 2], [2, 3], [10, 11], [11, 12], [12, 10]]],
        "tags": ["disjoint", "one-cyclic"],
    },
    {
        "id": "h08",
        "args": [[[1, 2], [3, 4], [5, 6], [7, 8]]],
        "tags": ["disjoint", "acyclic"],
    },
    {
        "id": "h09",
        "args": [[[1, 2], [1, 3], [2, 4], [3, 4], [4, 5]]],
        "tags": ["diamond", "acyclic"],
    },
    {
        "id": "h10",
        "args": [[[3, 1], [2, 3], [1, 2]]],
        "tags": ["cycle", "unsorted"],
    },
    {
        "id": "h11",
        "args": [[[1, 2], [2, 3], [1, 3], [3, 4], [2, 4]]],
        "tags": ["dag", "multiple-paths"],
    },
    {
        "id": "h12",
        "args": [[[1, 2], [1, 2], [2, 3]]],
        "tags": ["duplicate-edge", "acyclic"],
    },
    {
        "id": "h13",
        "args": [[[i, i + 1] for i in range(1, 60)] + [[60, 1]]],
        "tags": ["large", "long-cycle"],
    },
    {
        "id": "h14",
        "args": [[[i, i + 1] for i in range(1, 80)]],
        "tags": ["large", "acyclic"],
    },
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        nodes = 2 + (x >> 8) % 7
        x = _next(x)
        count = (x >> 8) % 10
        edges = []
        for _i in range(count):
            x = _next(x)
            a = 1 + (x >> 8) % nodes
            x = _next(x)
            b = 1 + (x >> 8) % nodes
            edges.append([a, b])
        out.append([edges])
    return out


for _i, _a in enumerate(_lcg(856, 10)):
    HIDDEN.append({"id": f"h{15 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
