"""Inputs of check-x683-fit-line; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3], [2, 4, 6]]},
    {"id": "s2", "args": [[1, 2, 3, 4], [2, 3, 5, 4]]},
]

HIDDEN = [
    {"id": "h01", "args": [[0, 1], [0, 1]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3, 4], [9, 7, 5, 3]], "tags": ["edge"]},
    {"id": "h03", "args": [[0, 1, 2, 3], [5, 5, 5, 5]], "tags": ["edge"]},
    {"id": "h04", "args": [[2, 4], [1, 7]], "tags": ["edge"]},
    {"id": "h05", "args": [[0, 1, 2], [1, 2, 6]], "tags": []},
    {"id": "h06", "args": [[-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]], "tags": []},
    {"id": "h07", "args": [[1, 2, 3, 4, 5], [2, 4, 5, 4, 5]], "tags": []},
    {"id": "h08", "args": [[10, 20, 30], [15, 25, 40]], "tags": []},
    {"id": "h09", "args": [[0.5, 1.5, 2.5], [1.0, 2.0, 4.5]], "tags": []},
    {"id": "h10", "args": [[3, 1, 2], [7, 3, 5]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = 2 + (x >> 8) % 8
        xs = []
        ys = []
        for i in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            xs.append(i * 2 + (x >> 8) % 2)
            x = (x * 1103515245 + 12345) % 2147483648
            ys.append((x >> 8) % 41 - 20)
        out.append([xs, ys])
    return out


for _i, _a in enumerate(_lcg(11, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
