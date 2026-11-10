"""Inputs of check-x880-simplify-order; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[3, 2], [100, 1], [50, 0]]]},
    {"id": "s2", "args": [[[0, 5], [7, 1]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[[0, 3], [0, 7]]], "tags": ["all-zero"]},
    {"id": "h03", "args": [[[1, 0]]], "tags": ["single", "constant"]},
    {"id": "h04", "args": [[[5, 4]]], "tags": ["single"]},
    {"id": "h05", "args": [[[3, 2], [100, 1], [50, 0]]], "tags": ["lower-dominated"]},
    {"id": "h06", "args": [[[2, 3], [9, 3], [4, 1]]], "tags": ["tie"]},
    {"id": "h07", "args": [[[1000000, 1], [1, 2]]], "tags": ["big-coeff"]},
    {"id": "h08", "args": [[[0, 9], [0, 1], [3, 0]]], "tags": ["zero-high-exp"]},
    {"id": "h09", "args": [[[1, 1000], [1, 999], [5, 0]]], "tags": ["large-exp"]},
    {"id": "h10", "args": [[[4, 1], [3, 5], [0, 8], [2, 2]]], "tags": ["unsorted"]},
    {"id": "h11", "args": [[[0, 0]]], "tags": ["zero-constant"]},
    {"id": "h12", "args": [[[7, 3], [7, 3], [7, 3]]], "tags": ["duplicates"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        m = (x >> 8) % 8
        terms = []
        for _i in range(m):
            x = _next(x)
            coeff = (x >> 8) % 4
            x = _next(x)
            exp = (x >> 8) % 12
            terms.append([coeff, exp])
        out.append([terms])
    return out


for _i, _a in enumerate(_lcg(880, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
