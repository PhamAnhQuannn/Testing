"""Inputs of check-x725-unique-order; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[3, 1, 3, 2, 1]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[7]], "tags": ["edge"]},
    {"id": "h03", "args": [[5, 5, 5, 5]], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 3, 4, 5]], "tags": ["edge"]},
    {"id": "h05", "args": [[-1, 2, -1, 0, 2, -3, 0]], "tags": ["edge"]},
    {"id": "h06", "args": [[4, 4, 1, 1, 4, 1, 9]], "tags": []},
    {"id": "h07", "args": [[9, 8, 7, 9, 8, 7, 9, 8, 7]], "tags": []},
    {"id": "h08", "args": [[0, 0, 0, 1, 0, 1, 2]], "tags": []},
    {"id": "h09", "args": [[10, -10, 10, -10, 0]], "tags": ["edge"]},
    {"id": "h10", "args": [[2, 1, 2, 3, 1, 4, 3, 5, 4, 6]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 15
        items = []
        for _j in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            items.append((x >> 8) % 9 - 3)
        out.append([items])
    return out


for _i, _a in enumerate(_lcg(25, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
