"""Inputs of check-x871-sstf-order; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[98, 183, 37, 122, 14, 124, 65, 67], 53]},
    {"id": "s2", "args": [[10, 20, 30], 25]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 0], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[42], 10], "tags": ["edge", "single"]},
    {"id": "h03", "args": [[5, 5, 5], 5], "tags": ["duplicates", "head-on-request"]},
    {"id": "h04", "args": [[30, 10, 20, 10], 25], "tags": ["duplicates", "tie"]},
    {"id": "h05", "args": [[60, 80, 70, 90], 10], "tags": ["all-above"]},
    {"id": "h06", "args": [[5, 3, 9, 1], 100], "tags": ["all-below"]},
    {"id": "h07", "args": [[10, 30], 20], "tags": ["tie"]},
    {"id": "h08", "args": [[0, 199, 100], 100], "tags": ["head-on-request"]},
    {"id": "h09", "args": [[1, 2, 3, 4, 5], 3], "tags": ["head-on-request", "tie"]},
    {"id": "h10", "args": [[50, 52, 48, 54, 46], 50], "tags": ["tie", "alternating"]},
    {"id": "h11", "args": [[7, 7, 1, 1, 13, 13], 7], "tags": ["duplicates"]},
    {"id": "h12", "args": [[0, 0], 0], "tags": ["edge", "zeros"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        nr = (x >> 8) % 9
        requests = []
        for _i in range(nr):
            x = _next(x)
            requests.append((x >> 8) % 50)
        x = _next(x)
        head = (x >> 8) % 50
        out.append([requests, head])
    return out


for _i, _a in enumerate(_lcg(871, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
