"""Inputs of check-x859-first-fit; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[100, 500, 200], [212, 417, 112, 426]]},
    {"id": "s2", "args": [[10, 20], [5, 5, 5]]},
]

HIDDEN = [
    {"id": "h01", "args": [[100, 200], []], "tags": ["edge", "empty-requests"]},
    {"id": "h02", "args": [[], [5]], "tags": ["edge", "no-blocks"]},
    {"id": "h03", "args": [[10, 20, 30], [50, 40, 31]], "tags": ["none-fit"]},
    {"id": "h04", "args": [[50, 60], [50, 60]], "tags": ["exact-fit"]},
    {"id": "h05", "args": [[50, 60], [50, 50, 10]], "tags": ["exact-fit", "consumed-block"]},
    {"id": "h06", "args": [[100], [60, 50, 40]], "tags": ["single-block", "forced-minus-one"]},
    {"id": "h07", "args": [[100], [30, 30, 30, 10, 1]], "tags": ["single-block"]},
    {"id": "h08", "args": [[5, 10, 3], [4, 4, 7, 2]], "tags": ["shrink"]},
    {"id": "h09", "args": [[0, 7, 0], [0, 7, 1]], "tags": ["zero-request"]},
    {"id": "h10", "args": [[300, 300, 300], [200, 200, 200, 200]], "tags": ["spread"]},
    {"id": "h11", "args": [[8, 4, 16, 2], [3, 3, 3, 3, 10, 6]], "tags": ["mixed"]},
    {"id": "h12", "args": [[1000, 1, 1000], [999, 2, 2, 1]], "tags": ["later-forced-minus-one"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        nb = (x >> 8) % 6
        blocks = []
        for _i in range(nb):
            x = _next(x)
            blocks.append((x >> 8) % 100)
        x = _next(x)
        nr = (x >> 8) % 8
        requests = []
        for _i in range(nr):
            x = _next(x)
            requests.append((x >> 8) % 70)
        out.append([blocks, requests])
    return out


for _i, _a in enumerate(_lcg(859, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
