"""Inputs of check-x707-nearest; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1.0, 0.0], [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]]},
    {"id": "s2", "args": [[1.0, 2.0], [[2.0, 4.0], [1.0, 0.0]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[1.0, 1.0], []], "tags": ["edge"]},
    {"id": "h02", "args": [[0.0, 0.0], [[1.0, 2.0], [3.0, 4.0]]], "tags": ["edge"]},
    {"id": "h03", "args": [[1.0, 0.0], [[0.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]], "tags": ["edge"]},
    {"id": "h04", "args": [[1.0, 0.0], [[0.0, 1.0], [2.0, 0.0], [1.0, 0.0]]], "tags": ["edge"]},
    {"id": "h05", "args": [[3.0, 4.0], [[4.0, 3.0], [3.0, 4.0], [0.0, 5.0]]], "tags": []},
    {"id": "h06", "args": [[0.0, 1.0], [[1.0, 0.0], [3.0, 3.0], [0.0, 5.0]]], "tags": []},
    {"id": "h07", "args": [[2.0], [[5.0]]], "tags": ["edge"]},
    {
        "id": "h08",
        "args": [[1.0, -1.0, 0.5], [[1.0, 1.0, 1.0], [-1.0, 1.0, -0.5], [2.0, -2.0, 1.0]]],
        "tags": [],
    },
    {"id": "h09", "args": [[1.0, 2.0, 3.0], [[-1.0, -2.0, -3.0], [-3.0, 0.0, 1.0]]], "tags": []},
    {
        "id": "h10",
        "args": [[5.0, 0.0, 1.0, 2.0], [[0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]]],
        "tags": ["edge"],
    },
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        d = 1 + (x >> 8) % 4
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + (x >> 8) % 5
        q = []
        for _j in range(d):
            x = (x * 1103515245 + 12345) % 2147483648
            q.append(float((x >> 8) % 9 - 4))
        items = []
        for _r in range(k):
            v = []
            for _j in range(d):
                x = (x * 1103515245 + 12345) % 2147483648
                v.append(float((x >> 8) % 9 - 4))
            items.append(v)
        out.append([q, items])
    return out


for _i, _a in enumerate(_lcg(29, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
