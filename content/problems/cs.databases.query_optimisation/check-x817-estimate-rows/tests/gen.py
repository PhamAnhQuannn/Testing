"""Inputs of check-x817-estimate-rows; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [1000, [[1, 2], [3, 10]]]},
    {"id": "s2", "args": [7, [[1, 2], [1, 2]]]},
]

HIDDEN = [
    {"id": "h01", "args": [500, []], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [0, [[1, 2], [3, 4]]], "tags": ["edge", "zero-rows"]},
    {"id": "h03", "args": [1000, [[0, 1]]], "tags": ["edge", "zero-selectivity"]},
    {"id": "h04", "args": [1000, [[1, 1], [5, 5]]], "tags": ["edge", "full-selectivity"]},
    {"id": "h05", "args": [10, [[1, 3]]], "tags": ["floor"]},
    {"id": "h06", "args": [99, [[1, 2], [1, 2], [1, 2]]], "tags": ["floor", "chain"]},
    {"id": "h07", "args": [2000, [[1, 4], [1, 10], [1, 3]]], "tags": ["chain"]},
    {"id": "h08", "args": [1, [[1, 2]]], "tags": ["edge", "floor-to-zero"]},
    {"id": "h09", "args": [1000000, [[1, 20], [2, 5], [9, 10], [1, 7]]], "tags": ["large"]},
    {"id": "h10", "args": [10000, [[3, 7], [7, 3 + 4]]], "tags": ["floor", "chain"]},
    {"id": "h11", "args": [9999, [[2, 3], [0, 5], [1, 1]]], "tags": ["zero-selectivity", "chain"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        rows = (x >> 8) % 10001
        x = (x * 1103515245 + 12345) % 2147483648
        k = (x >> 8) % 5
        sels = []
        for _r in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            den = (x >> 8) % 20 + 1
            x = (x * 1103515245 + 12345) % 2147483648
            num = (x >> 8) % (den + 1)
            sels.append([num, den])
        out.append([rows, sels])
    return out


for _i, _a in enumerate(_lcg(31, 10)):
    HIDDEN.append({"id": f"h{12 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
