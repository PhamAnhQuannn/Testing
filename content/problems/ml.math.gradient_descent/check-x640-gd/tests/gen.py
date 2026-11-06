"""Inputs of check-x640-gd; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3], [2, 4, 6], 0, 0.05, 20]},
    {"id": "s2", "args": [[1, 2, 3], [2, 4, 6], 0, 0.3, 3]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 4
        xs = []
        ys = []
        for _j in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            xv = (x >> 8) % 9 - 4
            x = (x * 1103515245 + 12345) % 2147483648
            yv = (x >> 8) % 21 - 10
            xs.append(xv)
            ys.append(yv)
        x = (x * 1103515245 + 12345) % 2147483648
        w0 = (x >> 8) % 11 - 5
        x = (x * 1103515245 + 12345) % 2147483648
        lr = ((x >> 8) % 5 + 1) / 100
        x = (x * 1103515245 + 12345) % 2147483648
        steps = (x >> 8) % 12
        out.append([xs, ys, w0, lr, steps])
    return out


HIDDEN = [
    {"id": "h01", "args": [[1, 2, 3], [2, 4, 6], 5, 0.1, 0], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3], [2, 4, 6], 0, 0.05, 20], "tags": ["converge"]},
    {"id": "h03", "args": [[1, 2, 3], [2, 4, 6], 2, 0.1, 10], "tags": ["edge"]},
    {"id": "h04", "args": [[2], [6], 0, 0.1, 5], "tags": ["single"]},
    {"id": "h05", "args": [[1, 2, 3], [2, 4, 6], 0, 0.3, 4], "tags": ["diverge"]},
    {"id": "h06", "args": [[1, 2, 3], [3, 5, 7], 1, 0.02, 50], "tags": ["converge"]},
    {"id": "h07", "args": [[1, 2], [1, 1], -3, 0.1, 30], "tags": ["converge"]},
    {"id": "h08", "args": [[1, 2, 3], [2, 4, 6], 0, 0.2, 100], "tags": ["converge"]},
]
for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
