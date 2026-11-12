"""Inputs of check-x892-cache-hits; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[0, 1, 0, 1], 4]},
    {"id": "s2", "args": [[0, 4, 0], 4]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 4], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[7], 4], "tags": ["single"]},
    {"id": "h03", "args": [[5, 5, 5], 8], "tags": ["same-addr"]},
    {"id": "h04", "args": [[0, 4, 0], 4], "tags": ["conflict"]},
    {"id": "h05", "args": [[0, 1, 2, 3, 0, 1, 2, 3], 4], "tags": ["second-pass-hits"]},
    {"id": "h06", "args": [[1, 2, 1, 1], 1], "tags": ["one-line"]},
    {
        "id": "h07",
        "args": [[1000000, 1000001, 1000000, 2000000], 1000000],
        "tags": ["large-addr"],
    },
    {"id": "h08", "args": [[0, 4, 8, 0, 4, 8], 4], "tags": ["thrash"]},
    {"id": "h09", "args": [[0, 1, 0, 1, 0, 1], 2], "tags": ["no-conflict"]},
    {"id": "h10", "args": [[2, 6, 2, 3, 3], 4], "tags": ["mixed"]},
    {"id": "h11", "args": [[0, 1, 2, 3, 4, 5, 6, 7], 8], "tags": ["all-miss"]},
    {"id": "h12", "args": [[0, 8, 16, 24, 0], 3], "tags": ["non-power-of-two"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        m = (x >> 8) % 25
        x = _next(x)
        lines = (x >> 8) % 8 + 1
        accesses = []
        for _i in range(m):
            x = _next(x)
            accesses.append((x >> 8) % 40)
        out.append([accesses, lines])
    return out


for _i, _a in enumerate(_lcg(892, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
