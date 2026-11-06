"""Inputs of check-x648-binomial; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [3, 2, 0.5]},
    {"id": "s2", "args": [5, 0, 0.2]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        nn = (x >> 8) % 21
        x = (x * 1103515245 + 12345) % 2147483648
        k = (x >> 8) % (nn + 3) - 1
        x = (x * 1103515245 + 12345) % 2147483648
        p = ((x >> 8) % 101) / 100
        out.append([nn, k, p])
    return out


HIDDEN = [
    {"id": "h01", "args": [5, 0, 0.2], "tags": ["edge"]},
    {"id": "h02", "args": [5, 5, 0.9], "tags": ["edge"]},
    {"id": "h03", "args": [6, 0, 0.0], "tags": ["edge"]},
    {"id": "h04", "args": [6, 3, 0.0], "tags": ["edge"]},
    {"id": "h05", "args": [6, 6, 1.0], "tags": ["edge"]},
    {"id": "h06", "args": [6, 2, 1.0], "tags": ["edge"]},
    {"id": "h07", "args": [4, 5, 0.5], "tags": ["edge", "out_of_range"]},
    {"id": "h08", "args": [4, -1, 0.5], "tags": ["edge", "out_of_range"]},
    {"id": "h09", "args": [0, 0, 0.3], "tags": ["edge"]},
    {"id": "h10", "args": [10, 3, 0.3], "tags": []},
    {"id": "h11", "args": [3, 2, 0.5], "tags": []},
    {"id": "h12", "args": [20, 10, 0.5], "tags": []},
]
for _i, _a in enumerate(_lcg(7, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
