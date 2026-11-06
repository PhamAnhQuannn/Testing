"""Inputs of check-x673-ece; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[100, 0.2, 0.1], [200, 0.5, 0.4], [100, 0.8, 0.6]]]},
    {"id": "s2", "args": [[[10, 0.9, 0.5]]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 5
        bins = []
        for _j in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            cnt = (x >> 8) % 200
            x = (x * 1103515245 + 12345) % 2147483648
            conf = ((x >> 8) % 101) / 100
            x = (x * 1103515245 + 12345) % 2147483648
            acc = ((x >> 8) % 101) / 100
            bins.append([cnt, conf, acc])
        out.append([bins])
    return out


HIDDEN = [
    {"id": "h01", "args": [[[50, 0.3, 0.3], [50, 0.7, 0.7]]], "tags": ["perfect"]},
    {"id": "h02", "args": [[[80, 0.8, 0.6]]], "tags": ["single"]},
    {"id": "h03", "args": [[]], "tags": ["edge"]},
    {"id": "h04", "args": [[[0, 0.5, 0.5], [0, 0.9, 0.1]]], "tags": ["edge", "zero-count"]},
    {"id": "h05", "args": [[[100, 0.9, 0.7], [100, 0.95, 0.8], [50, 0.99, 0.9]]], "tags": ["over"]},
    {"id": "h06", "args": [[[30, 0.1, 0.3], [70, 0.4, 0.6]]], "tags": ["under"]},
    {"id": "h07", "args": [[[100, 0.2, 0.1], [200, 0.5, 0.4], [100, 0.8, 0.6]]], "tags": ["mixed"]},
    {"id": "h08", "args": [[[50, 0.1, 0.2], [150, 0.6, 0.5], [100, 0.9, 0.7]]], "tags": ["mixed"]},
]
for _i, _a in enumerate(_lcg(11, 8)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
