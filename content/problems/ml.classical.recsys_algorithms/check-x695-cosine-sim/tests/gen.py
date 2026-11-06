"""Inputs of check-x695-cosine-sim; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1.0, 0.0], [1.0, 0.0]]},
    {"id": "s2", "args": [[1.0, 0.0], [0.0, 1.0]]},
]

HIDDEN = [
    {"id": "h01", "args": [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], "tags": ["edge"]},
    {"id": "h02", "args": [[1.0, 0.0, 0.0], [0.0, 5.0, 0.0]], "tags": ["edge"]},
    {"id": "h03", "args": [[0.0, 0.0], [3.0, 4.0]], "tags": ["edge"]},
    {"id": "h04", "args": [[1.0, -2.0], [-1.0, 2.0]], "tags": ["edge"]},
    {"id": "h05", "args": [[3.0, 4.0], [4.0, 3.0]], "tags": []},
    {"id": "h06", "args": [[1.0, 1.0, 0.0], [0.0, 1.0, 1.0]], "tags": []},
    {"id": "h07", "args": [[2.0], [5.0]], "tags": []},
    {"id": "h08", "args": [[0.5, 1.5, -1.0], [2.0, -1.0, 0.5]], "tags": []},
    {"id": "h09", "args": [[5.0, 0.0, 1.0, 2.0], [0.0, 0.0, 0.0, 0.0]], "tags": ["edge"]},
    {"id": "h10", "args": [[1.0, 2.0, 3.0, 4.0], [2.0, 4.0, 6.0, 8.0]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = 1 + (x >> 8) % 8
        a = []
        b = []
        for _j in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            a.append(float((x >> 8) % 11 - 5))
            x = (x * 1103515245 + 12345) % 2147483648
            b.append(float((x >> 8) % 11 - 5))
        out.append([a, b])
    return out


for _i, _a in enumerate(_lcg(23, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
