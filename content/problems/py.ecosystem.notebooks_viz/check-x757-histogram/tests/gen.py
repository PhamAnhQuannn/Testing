"""Inputs of check-x757-histogram; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4], 2]},
    {"id": "s2", "args": [[5, 5, 5], 3]},
]

HIDDEN = [
    {"id": "h01", "args": [[7], 1], "tags": ["edge"]},
    {"id": "h02", "args": [[7], 4], "tags": ["edge"]},
    {"id": "h03", "args": [[3, 3, 3, 3], 5], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 5, 2, 9, 3], 1], "tags": ["edge"]},
    {"id": "h05", "args": [[-5, -3, -1, 0, 4, -2], 3], "tags": ["edge"]},
    {"id": "h06", "args": [[0, 5, 10], 2], "tags": ["edge"]},
    {"id": "h07", "args": [[0, 2, 4, 6, 8, 10], 5], "tags": ["edge"]},
    {"id": "h08", "args": [[1, 2], 10], "tags": ["edge"]},
    {"id": "h09", "args": [[1, 1, 2, 2, 3, 3, 4, 4], 4], "tags": []},
    {"id": "h10", "args": [[-10, 10, 0, -10, 10], 4], "tags": ["edge"]},
    {"id": "h11", "args": [[0, 100, 50, 25, 75, 100], 20], "tags": ["edge"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_vals = 1 + (x >> 8) % 15
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 8
        values = []
        for _r in range(n_vals):
            x = (x * 1103515245 + 12345) % 2147483648
            values.append((x >> 8) % 41 - 20)
        out.append([values, k])
    return out


for _i, _a in enumerate(_lcg(29, 10)):
    HIDDEN.append({"id": f"h{12 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
