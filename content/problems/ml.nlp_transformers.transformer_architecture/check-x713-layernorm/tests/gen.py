"""Inputs of check-x713-layernorm; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1.0, 2.0, 3.0]]},
    {"id": "s2", "args": [[5.0, 5.0]]},
]

HIDDEN = [
    {"id": "h01", "args": [[7.0, 7.0, 7.0, 7.0]], "tags": ["edge"]},
    {"id": "h02", "args": [[3.0]], "tags": ["edge"]},
    {"id": "h03", "args": [[-1.0, -2.0, -3.0]], "tags": ["edge"]},
    {"id": "h04", "args": [[0.0, 4.0]], "tags": []},
    {"id": "h05", "args": [[2.0, 4.0, 6.0, 8.0]], "tags": []},
    {"id": "h06", "args": [[-1.0, 1.0]], "tags": ["edge"]},
    {"id": "h07", "args": [[0.5, 1.5, -1.0, 2.0]], "tags": []},
    {"id": "h08", "args": [[100.0, 200.0, 300.0]], "tags": []},
    {"id": "h09", "args": [[0.0, 0.0, 0.0, 1.0]], "tags": []},
    {"id": "h10", "args": [[2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = 1 + (x >> 8) % 8
        v = []
        for _j in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            v.append(float((x >> 8) % 21 - 10))
        out.append([v])
    return out


for _i, _a in enumerate(_lcg(31, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
