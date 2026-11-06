"""Inputs of check-x667-mse; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[2, 4, 6], [3, 4, 9]]},
    {"id": "s2", "args": [[1.5, 2.5], [1.0, 3.5]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 6
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
    {"id": "h02", "args": [[5], [2]], "tags": ["single"]},
    {"id": "h03", "args": [[], []], "tags": ["edge"]},
    {"id": "h04", "args": [[-1, -2, -3], [1, 2, 3]], "tags": ["negative"]},
    {"id": "h05", "args": [[1000000, 2000000], [1000001, 1999998]], "tags": ["large"]},
    {"id": "h06", "args": [[0.5, 1.5, 2.5], [0.25, 1.75, 2.0]], "tags": ["float"]},
]
for _i, _a in enumerate(_lcg(7, 8)):
    HIDDEN.append({"id": f"h{7 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
