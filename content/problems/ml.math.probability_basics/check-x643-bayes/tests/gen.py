"""Inputs of check-x643-bayes; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [0.01, 0.99, 0.05]},
    {"id": "s2", "args": [0.5, 0.9, 0.1]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        vals = []
        for _j in range(3):
            x = (x * 1103515245 + 12345) % 2147483648
            vals.append(((x >> 8) % 101) / 100)
        out.append(vals)
    return out


HIDDEN = [
    {"id": "h01", "args": [0.0, 0.9, 0.1], "tags": ["edge"]},
    {"id": "h02", "args": [1.0, 0.5, 0.5], "tags": ["edge"]},
    {"id": "h03", "args": [0.3, 0.8, 0.0], "tags": ["edge"]},
    {"id": "h04", "args": [0.0, 0.9, 0.0], "tags": ["edge"]},
    {"id": "h05", "args": [0.2, 0.0, 0.0], "tags": ["edge"]},
    {"id": "h06", "args": [1.0, 0.0, 0.7], "tags": ["edge"]},
    {"id": "h07", "args": [0.01, 0.99, 0.05], "tags": ["base-rate"]},
    {"id": "h08", "args": [0.001, 0.95, 0.02], "tags": ["base-rate"]},
    {"id": "h09", "args": [0.5, 0.9, 0.1], "tags": []},
    {"id": "h10", "args": [0.3, 0.6, 0.6], "tags": ["independent"]},
]
for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
