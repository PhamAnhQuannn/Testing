"""Inputs of check-x687-gini; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[0, 0, 1, 1]]},
    {"id": "s2", "args": [[1, 1, 1]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[5]], "tags": ["edge"]},
    {"id": "h03", "args": [[0, 1]], "tags": ["edge"]},
    {"id": "h04", "args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], "tags": ["edge"]},
    {"id": "h05", "args": [[0, 0, 0, 1]], "tags": ["skewed"]},
    {"id": "h06", "args": [[0, 0, 1, 1, 2, 2]], "tags": ["multi"]},
    {"id": "h07", "args": [[3, 3, 3, 3, 3, 3]], "tags": ["pure"]},
    {"id": "h08", "args": [[0, 0, 0, 1, 1, 1]], "tags": ["half"]},
    {"id": "h09", "args": [[1, 2, 2, 3, 3, 3]], "tags": ["multi"]},
    {"id": "h10", "args": [[-1, -1, 1, 1, 1]], "tags": ["negative"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        size = (x >> 8) % 40
        classes = 1 + (x >> 16) % 5
        labels = []
        for _j in range(size):
            x = (x * 1103515245 + 12345) % 2147483648
            labels.append((x >> 8) % classes)
        out.append([labels])
    return out


for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
