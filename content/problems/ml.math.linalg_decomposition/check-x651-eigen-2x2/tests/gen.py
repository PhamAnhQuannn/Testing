"""Inputs of check-x651-eigen-2x2; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[2, 1], [1, 2]]]},
    {"id": "s2", "args": [[[2, 0], [0, 1]]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        row = []
        for _j in range(4):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append((x >> 8) % 11 - 5)
        out.append([[row[0], row[1]], [row[2], row[3]]])
    return out


HIDDEN = [
    {"id": "h01", "args": [[[3, 0], [0, -2]]], "tags": ["diagonal"]},
    {"id": "h02", "args": [[[2, 1], [1, 2]]], "tags": ["symmetric"]},
    {"id": "h03", "args": [[[4, 0], [0, 4]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[0, -1], [1, 0]]], "tags": ["edge"]},
    {"id": "h05", "args": [[[-2, 1], [1, -2]]], "tags": ["negative"]},
    {"id": "h06", "args": [[[1, 2], [2, 4]]], "tags": ["singular"]},
    {"id": "h07", "args": [[[2, 1], [0, 2]]], "tags": ["edge"]},
    {"id": "h08", "args": [[[1, 2], [3, 4]]], "tags": []},
    {"id": "h09", "args": [[[0, 0], [0, 0]]], "tags": ["edge"]},
]
for _i, _a in enumerate(_lcg(7, 10)):
    HIDDEN.append({"id": f"h{10 + _i:02d}", "args": [_a], "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": [a]} for i, a in enumerate(_lcg(seed, n))]
