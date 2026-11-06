"""Inputs of check-x716-causal-mask; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [3]},
    {"id": "s2", "args": [1]},
]

HIDDEN = [
    {"id": "h01", "args": [1], "tags": ["edge"]},
    {"id": "h02", "args": [2], "tags": ["edge"]},
    {"id": "h03", "args": [3], "tags": []},
    {"id": "h04", "args": [4], "tags": []},
    {"id": "h05", "args": [5], "tags": []},
    {"id": "h06", "args": [7], "tags": []},
    {"id": "h07", "args": [10], "tags": []},
    {"id": "h08", "args": [16], "tags": []},
    {"id": "h09", "args": [30], "tags": []},
    {"id": "h10", "args": [100], "tags": ["edge"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append([1 + (x >> 8) % 20])
    return out


for _i, _a in enumerate(_lcg(17, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
