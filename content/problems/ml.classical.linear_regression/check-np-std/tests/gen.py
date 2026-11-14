"""Inputs of check-np-std; `expected` comes from solution.py (numpy) via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]]},
    {"id": "s2", "args": [[1.0, 2.0, 3.0]]},
]

HIDDEN = [
    {"id": "h01", "args": [[5.0]], "tags": ["edge"]},
    {"id": "h02", "args": [[3.0, 3.0, 3.0]], "tags": ["edge"]},
    {"id": "h03", "args": [[0.0, 10.0]], "tags": ["edge"]},
    {"id": "h04", "args": [[-1.5, 2.5, 0.0, 4.0]], "tags": []},
    {"id": "h05", "args": [[1.0, 2.0, 3.0, 4.0, 5.0]], "tags": []},
    {"id": "h06", "args": [[100.0, 200.0, 300.0]], "tags": []},
    {"id": "h07", "args": [[0.1, 0.2, 0.3, 0.4]], "tags": []},
    {"id": "h08", "args": [[-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = 2 + (x >> 8) % 8
        xs = []
        for _ in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            xs.append(float((x >> 8) % 41 - 20))
        out.append([xs])
    return out


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
