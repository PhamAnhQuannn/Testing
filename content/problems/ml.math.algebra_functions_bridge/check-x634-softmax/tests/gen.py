"""Inputs of check-x634-softmax; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3]]},
    {"id": "s2", "args": [[0, 0]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        size = 1 + (x >> 8) % 6
        xs = []
        for _ in range(size):
            x = (x * 1103515245 + 12345) % 2147483648
            xs.append((x >> 8) % 41 - 20)
        out.append([xs])
    return out


HIDDEN = [
    {"id": "h01", "args": [[5]], "tags": ["edge"]},
    {"id": "h02", "args": [[0, 0, 0, 0]], "tags": ["edge"]},
    {"id": "h03", "args": [[-1, -2, -3]], "tags": ["negative"]},
    {"id": "h04", "args": [[1000, 1001, 1002]], "tags": ["stability"]},
    {"id": "h05", "args": [[-1000, -1001]], "tags": ["stability"]},
    {"id": "h06", "args": [[2, -2]], "tags": ["basic"]},
    {"id": "h07", "args": [[0, 1]], "tags": ["basic"]},
    {"id": "h08", "args": [[1.5, 2.5, 0.5]], "tags": ["float"]},
    {"id": "h09", "args": [[700, 0]], "tags": ["stability"]},
]
for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{10 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
