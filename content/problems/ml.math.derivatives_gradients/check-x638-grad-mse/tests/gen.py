"""Inputs of check-x638-grad-mse; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [3, [2], [1]]},
    {"id": "s2", "args": [1, [1, 2, 3], [2, 4, 6]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 6
        x = (x * 1103515245 + 12345) % 2147483648
        w = (x >> 8) % 11 - 5
        xs = []
        ys = []
        for _ in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            xs.append((x >> 8) % 13 - 6)
            x = (x * 1103515245 + 12345) % 2147483648
            ys.append((x >> 8) % 21 - 10)
        out.append([w, xs, ys])
    return out


HIDDEN = [
    {"id": "h01", "args": [2, [1, 2, 3], [2, 4, 6]], "tags": ["edge"]},
    {"id": "h02", "args": [0, [1, 2, 3], [1, 2, 3]], "tags": ["edge"]},
    {"id": "h03", "args": [3, [2], [1]], "tags": ["single"]},
    {"id": "h04", "args": [1, [1, 2], [5, 8]], "tags": ["negative"]},
    {"id": "h05", "args": [-2, [1, -1, 2], [3, 1, -4]], "tags": ["negative-w"]},
    {"id": "h06", "args": [0.5, [1.5, 2.5, -1.0], [1.0, 2.0, 0.5]], "tags": ["float"]},
    {"id": "h07", "args": [4, [0, 0, 0], [1, 2, 3]], "tags": ["zero-x"]},
    {"id": "h08", "args": [1, [1, 2, 3, 4], [1, 2, 3, 4]], "tags": ["perfect"]},
]
for _i, _a in enumerate(_lcg(11, 12)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
