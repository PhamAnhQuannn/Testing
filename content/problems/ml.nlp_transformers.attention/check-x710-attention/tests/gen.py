"""Inputs of check-x710-attention; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]]},
    {"id": "s2", "args": [[1.0, 1.0], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[3.0, 4.0], [[1.0, 1.0]]], "tags": ["edge"]},
    {"id": "h02", "args": [[0.0, 0.0], [[1.0, 2.0], [3.0, 4.0]]], "tags": ["edge"]},
    {"id": "h03", "args": [[1.0], [[0.0], [1.0], [2.0]]], "tags": []},
    {"id": "h04", "args": [[50.0, 50.0], [[10.0, 10.0], [0.0, 0.0], [5.0, 5.0]]], "tags": ["edge"]},
    {"id": "h05", "args": [[-1.0, 2.0], [[1.0, 0.0], [0.0, 1.0], [-1.0, 1.0]]], "tags": []},
    {"id": "h06", "args": [[1.0, 2.0, 3.0], [[3.0, 2.0, 1.0], [1.0, 2.0, 3.0]]], "tags": []},
    {
        "id": "h07",
        "args": [[0.5, -0.5], [[2.0, 0.0], [0.0, 2.0], [1.0, 1.0], [-1.0, 1.0]]],
        "tags": [],
    },
    {"id": "h08", "args": [[-30.0, -30.0], [[10.0, 10.0], [-10.0, -10.0]]], "tags": ["edge"]},
    {
        "id": "h09",
        "args": [
            [2.0, 0.0, 1.0, 0.0],
            [[1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0], [2.0, 0.0, 0.0, 1.0]],
        ],
        "tags": [],
    },
    {"id": "h10", "args": [[1.5], [[1.0], [1.0], [-2.0], [0.5], [3.0]]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        d = 1 + (x >> 8) % 4
        x = (x * 1103515245 + 12345) % 2147483648
        m = 1 + (x >> 8) % 6
        q = []
        for _j in range(d):
            x = (x * 1103515245 + 12345) % 2147483648
            q.append(float((x >> 8) % 9 - 4) / 2.0)
        keys = []
        for _k in range(m):
            key = []
            for _j in range(d):
                x = (x * 1103515245 + 12345) % 2147483648
                key.append(float((x >> 8) % 9 - 4) / 2.0)
            keys.append(key)
        out.append([q, keys])
    return out


for _i, _a in enumerate(_lcg(29, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
