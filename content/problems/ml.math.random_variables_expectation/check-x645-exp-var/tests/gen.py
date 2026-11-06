"""Inputs of check-x645-exp-var; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[0, 1], [0.5, 0.5]]},
    {"id": "s2", "args": [[1, 2, 3, 4], [0.25, 0.25, 0.25, 0.25]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 5
        xs = []
        ws = []
        for _j in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            xs.append((x >> 8) % 21 - 10)
            x = (x * 1103515245 + 12345) % 2147483648
            ws.append(1 + (x >> 8) % 9)
        total = sum(ws)
        ps = [round(w / total, 6) for w in ws]
        out.append([xs, ps])
    return out


HIDDEN = [
    {"id": "h01", "args": [[0, 1], [0.5, 0.5]], "tags": ["two-point"]},
    {"id": "h02", "args": [[7], [1.0]], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3, 4], [0.25, 0.25, 0.25, 0.25]], "tags": ["uniform"]},
    {"id": "h04", "args": [[0, 10], [0.9, 0.1]], "tags": ["skewed"]},
    {"id": "h05", "args": [[-1, 0, 1], [0.25, 0.5, 0.25]], "tags": ["symmetric"]},
    {"id": "h06", "args": [[0, 1, 2], [0.5, 0.25, 0.25]], "tags": []},
    {"id": "h07", "args": [[5, 5, 5], [0.2, 0.3, 0.5]], "tags": ["edge"]},
    {"id": "h08", "args": [[-4, 3], [0.125, 0.875]], "tags": ["skewed"]},
]
for _i, _a in enumerate(_lcg(7, 10)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
