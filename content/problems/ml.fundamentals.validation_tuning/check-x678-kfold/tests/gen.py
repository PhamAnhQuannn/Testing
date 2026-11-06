"""Inputs of check-x678-kfold; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [10, 3]},
    {"id": "s2", "args": [6, 2]},
]

HIDDEN = [
    {"id": "h01", "args": [1, 1], "tags": ["edge"]},
    {"id": "h02", "args": [7, 1], "tags": ["edge"]},
    {"id": "h03", "args": [5, 5], "tags": ["edge"]},
    {"id": "h04", "args": [12, 4], "tags": ["even"]},
    {"id": "h05", "args": [10, 3], "tags": ["uneven"]},
    {"id": "h06", "args": [7, 2], "tags": ["uneven"]},
    {"id": "h07", "args": [11, 5], "tags": ["uneven"]},
    {"id": "h08", "args": [100, 7], "tags": ["large"]},
    {"id": "h09", "args": [9, 8], "tags": ["uneven"]},
    {"id": "h10", "args": [20, 2], "tags": ["even"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        total = 1 + (x >> 8) % 30
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % total
        out.append([total, k])
    return out


for _i, _a in enumerate(_lcg(7, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
