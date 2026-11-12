"""Inputs of check-x889-decode-twos; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 0, 0, 0]]},
    {"id": "s2", "args": [[0, 1, 0, 1]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[0]], "tags": ["single", "zero"]},
    {"id": "h03", "args": [[1]], "tags": ["single", "negative"]},
    {"id": "h04", "args": [[1, 0, 0, 0]], "tags": ["min"]},
    {"id": "h05", "args": [[1, 1, 1, 1]], "tags": ["all-ones"]},
    {"id": "h06", "args": [[0, 1, 0, 1]], "tags": ["positive"]},
    {"id": "h07", "args": [[0, 0, 0, 0]], "tags": ["all-zero"]},
    {"id": "h08", "args": [[0, 1, 1, 1]], "tags": ["max"]},
    {"id": "h09", "args": [[1, 0, 0, 0, 0, 0, 0, 0]], "tags": ["min", "width8"]},
    {"id": "h10", "args": [[1, 1, 1, 1, 1, 1, 1, 1]], "tags": ["all-ones", "width8"]},
    {"id": "h11", "args": [[0, 1, 1, 1, 1, 1, 1, 1]], "tags": ["max", "width8"]},
    {"id": "h12", "args": [[1, 0, 1, 1, 0, 1, 0, 0]], "tags": ["negative", "mixed"]},
    {"id": "h13", "args": [[0, 0, 1, 0, 1, 1, 0, 1]], "tags": ["positive", "mixed"]},
    {"id": "h14", "args": [[0, 0, 0]], "tags": ["all-zero", "width3"]},
    {"id": "h15", "args": [[1, 1, 1]], "tags": ["all-ones", "width3"]},
    {"id": "h16", "args": [[1, 0]], "tags": ["width2"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        width = 1 + (x >> 8) % 16
        bits = []
        for _i in range(width):
            x = _next(x)
            bits.append((x >> 8) % 2)
        out.append([bits])
    return out


for _i, _a in enumerate(_lcg(889, 10)):
    HIDDEN.append({"id": f"h{17 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
