"""Inputs of check-x692-evr; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[4.0, 1.0]]},
    {"id": "s2", "args": [[1, 1, 2]]},
]

HIDDEN = [
    {"id": "h01", "args": [[5.0]], "tags": ["edge"]},
    {"id": "h02", "args": [[2, 2, 2, 2]], "tags": ["edge"]},
    {"id": "h03", "args": [[3.0, 0, 1.0]], "tags": ["edge"]},
    {"id": "h04", "args": [[0, 0, 0]], "tags": ["edge"]},
    {"id": "h05", "args": [[1, 2, 3, 4]], "tags": []},
    {"id": "h06", "args": [[0.5, 0.25, 0.125]], "tags": []},
    {"id": "h07", "args": [[10, 1]], "tags": []},
    {"id": "h08", "args": [[1, 1, 1]], "tags": []},
    {"id": "h09", "args": [[7.5, 2.5, 0.0, 0.0]], "tags": ["edge"]},
    {"id": "h10", "args": [[100, 50, 25, 12.5, 6.25]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = 1 + (x >> 8) % 8
        vs = []
        for _j in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            vs.append(((x >> 8) % 400) / 10)
        out.append([vs])
    return out


for _i, _a in enumerate(_lcg(17, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
