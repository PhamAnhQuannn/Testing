"""Inputs of check-x654-nll; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 0, 1], [0.9, 0.2, 0.6]]},
    {"id": "s2", "args": [[1, 1, 0, 0], [0.5, 0.5, 0.5, 0.5]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = 1 + (x >> 8) % 6
        ys = []
        ps = []
        for _j in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            ys.append((x >> 8) % 2)
            x = (x * 1103515245 + 12345) % 2147483648
            ps.append((1 + (x >> 8) % 99) / 100)
        out.append([ys, ps])
    return out


HIDDEN = [
    {
        "id": "h01",
        "args": [[1, 0, 1, 0], [0.999999, 0.000001, 0.999999, 0.000001]],
        "tags": ["edge"],
    },
    {"id": "h02", "args": [[1, 0], [0.01, 0.99]], "tags": ["edge"]},
    {"id": "h03", "args": [[1], [0.5]], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 1, 1], [0.9, 0.95, 0.99]], "tags": []},
    {"id": "h05", "args": [[1, 0], [1.0, 0.0]], "tags": ["edge", "clamp"]},
    {"id": "h06", "args": [[0, 0, 0], [0.1, 0.1, 0.1]], "tags": []},
    {"id": "h07", "args": [[1, 0, 1, 1, 0], [0.7, 0.3, 0.7, 0.7, 0.3]], "tags": []},
    {"id": "h08", "args": [[1, 0, 1], [0.9, 0.2, 0.6]], "tags": []},
]
for _i, _a in enumerate(_lcg(31, 10)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
