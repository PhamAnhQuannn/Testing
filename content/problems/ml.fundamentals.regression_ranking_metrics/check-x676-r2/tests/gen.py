"""Inputs of check-x676-r2; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[3, 5, 7], [2, 5, 9]]},
    {"id": "s2", "args": [[1, 2, 3, 4], [1.5, 1.5, 3.5, 3.5]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = 2 + (x >> 8) % 6
        yt = []
        yp = []
        for _j in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            yt.append((x >> 8) % 41 - 20)
            x = (x * 1103515245 + 12345) % 2147483648
            yp.append((x >> 8) % 41 - 20)
        out.append([yt, yp])
    return out


HIDDEN = [
    {"id": "h01", "args": [[1, 2, 3], [1, 2, 3]], "tags": ["perfect"]},
    {"id": "h02", "args": [[4, 4, 4], [3, 4, 5]], "tags": ["edge", "constant"]},
    {"id": "h03", "args": [[1, 2, 3], [3, 3, 3]], "tags": ["worse"]},
    {"id": "h04", "args": [[1, 2, 3], [3, 1, 0]], "tags": ["negative"]},
    {"id": "h05", "args": [[7], [5]], "tags": ["single", "edge"]},
    {"id": "h06", "args": [[3, 5, 7], [2, 5, 9]], "tags": ["mixed"]},
    {"id": "h07", "args": [[0.5, 1.5, 2.5, 4.0], [0.0, 2.0, 2.0, 5.0]], "tags": ["float"]},
    {"id": "h08", "args": [[], []], "tags": ["edge", "empty"]},
]
for _i, _a in enumerate(_lcg(11, 8)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
