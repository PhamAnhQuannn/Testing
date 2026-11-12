"""Inputs of check-x895-xor-cipher; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[65, 66, 67], [7]]},
    {"id": "s2", "args": [[1, 2, 3, 4], [1, 2]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [5]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[65, 66, 67], [7]], "tags": ["single-key"]},
    {"id": "h03", "args": [[1, 2, 3, 4], [1, 2]], "tags": ["wrap"]},
    {"id": "h04", "args": [[255, 0], [255]], "tags": ["edge", "255"]},
    {"id": "h05", "args": [[10, 20], [1, 2, 3, 4, 5]], "tags": ["key-longer"]},
    {"id": "h06", "args": [[9, 8, 7], [0]], "tags": ["zero-key"]},
    {"id": "h07", "args": [[0, 0, 0, 0], [13, 14]], "tags": ["zero-data"]},
    {"id": "h08", "args": [[7, 7, 7, 7, 7], [7]], "tags": ["self-cancel"]},
    {"id": "h09", "args": [[70, 69, 68], [7]], "tags": ["round-trip"]},
    {"id": "h10", "args": [[0, 255, 0, 255, 0], [255, 0]], "tags": ["edge"]},
    {"id": "h11", "args": [[5, 5, 5], [1, 2]], "tags": ["wrap"]},
    {"id": "h12", "args": [[100], [100, 200]], "tags": ["single", "key-longer"]},
    {"id": "h13", "args": [[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3]], "tags": ["wrap", "multi"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        m = (x >> 8) % 16
        data = []
        for _i in range(m):
            x = _next(x)
            data.append((x >> 8) % 256)
        x = _next(x)
        kl = (x >> 8) % 6 + 1
        key = []
        for _j in range(kl):
            x = _next(x)
            key.append((x >> 8) % 256)
        out.append([data, key])
    return out


for _i, _a in enumerate(_lcg(895, 10)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
