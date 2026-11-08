"""Inputs of check-x850-semaphore; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["P", "P", "V", "P"], 1]},
    {"id": "s2", "args": [["V", "V"], 0]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[], 0], "tags": ["edge", "empty"]},
    {"id": "h03", "args": [["V", "V", "V"], 0], "tags": ["all-v"]},
    {"id": "h04", "args": [["V"], 5], "tags": ["all-v", "initial"]},
    {"id": "h05", "args": [["P"], 0], "tags": ["edge", "blocked"]},
    {"id": "h06", "args": [["P", "P", "P"], 0], "tags": ["all-blocked"]},
    {"id": "h07", "args": [["P", "P", "P"], 3], "tags": ["drain"]},
    {"id": "h08", "args": [["P", "P", "P", "P", "P"], 2], "tags": ["drain-then-blocked"]},
    {"id": "h09", "args": [["P", "V", "P", "V"], 0], "tags": ["mixed", "restore"]},
    {"id": "h10", "args": [["P", "P", "V", "V", "P", "P"], 1], "tags": ["mixed"]},
    {"id": "h11", "args": [["P", "P", "V", "P", "P", "V", "V"], 0], "tags": ["blocked-not-queued"]},
    {"id": "h12", "args": [["V", "P", "P", "P", "V", "P"], 1], "tags": ["mixed"]},
    {"id": "h13", "args": [["P"] * 6 + ["V"] * 3, 2], "tags": ["blocks-then-restore"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        initial = (x >> 8) % 4
        x = _next(x)
        count = (x >> 8) % 13
        ops = []
        for _r in range(count):
            x = _next(x)
            ops.append("P" if (x >> 8) % 2 == 0 else "V")
        out.append([ops, initial])
    return out


for _i, _a in enumerate(_lcg(53, 10)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
