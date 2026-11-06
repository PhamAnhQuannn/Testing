"""Inputs of check-x660-ci; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [0.05, 10000]},
    {"id": "s2", "args": [0.5, 100]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        p = ((x >> 8) % 101) / 100
        x = (x * 1103515245 + 12345) % 2147483648
        size = 1 + ((x >> 8) % 5000)
        out.append([p, size])
    return out


HIDDEN = [
    {"id": "h01", "args": [0.0, 100], "tags": ["edge"]},
    {"id": "h02", "args": [1.0, 100], "tags": ["edge"]},
    {"id": "h03", "args": [0.5, 1], "tags": ["edge"]},
    {"id": "h04", "args": [0.5, 100], "tags": ["widest"]},
    {"id": "h05", "args": [0.05, 10000], "tags": []},
    {"id": "h06", "args": [0.054, 10000], "tags": []},
    {"id": "h07", "args": [0.3, 1000000], "tags": ["large-n"]},
    {"id": "h08", "args": [0.1, 25], "tags": ["small-n"]},
    {"id": "h09", "args": [0.02, 400], "tags": []},
    {"id": "h10", "args": [0.9, 50], "tags": []},
]
for _i, _a in enumerate(_lcg(31, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
