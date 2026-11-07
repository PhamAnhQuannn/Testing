"""Inputs of check-x749-dot-product; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3], [4, 5, 6]]},
    {"id": "s2", "args": [[], []]},
]

HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[5], [7]], "tags": ["edge", "single"]},
    {"id": "h03", "args": [[0, 0, 0], [4, 5, 6]], "tags": ["edge", "zeros"]},
    {"id": "h04", "args": [[-1, -2, -3], [4, 5, 6]], "tags": ["edge", "negatives"]},
    {"id": "h05", "args": [[1, -1, 1, -1], [1, 1, 1, 1]], "tags": ["negatives"]},
    {"id": "h06", "args": [[2, 3], [0, 0]], "tags": ["zeros"]},
    {"id": "h07", "args": [[10, 20, 30], [1, 2, 3]], "tags": []},
    {"id": "h08", "args": [[-7], [-6]], "tags": ["edge", "single", "negatives"]},
    {"id": "h09", "args": [[1, 0, 0, 0], [0, 0, 0, 1]], "tags": ["zeros"]},
    {"id": "h10", "args": [[100, 200, 300, 400, 500], [5, 4, 3, 2, 1]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 9
        a = []
        b = []
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            a.append((x >> 8) % 19 - 9)
            x = (x * 1103515245 + 12345) % 2147483648
            b.append((x >> 8) % 19 - 9)
        out.append([a, b])
    return out


for _i, _a in enumerate(_lcg(17, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
