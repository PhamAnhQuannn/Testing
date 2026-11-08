"""Inputs of check-x853-fcfs-waiting; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[0, 4], [1, 3], [2, 1]]]},
    {"id": "s2", "args": [[[2, 2], [0, 3]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[[5, 2]]], "tags": ["edge", "single", "idle"]},
    {"id": "h03", "args": [[[0, 3], [0, 2], [0, 4]]], "tags": ["all-at-zero"]},
    {"id": "h04", "args": [[[2, 2], [0, 3]]], "tags": ["out-of-order"]},
    {"id": "h05", "args": [[[0, 2], [10, 3], [11, 1]]], "tags": ["idle-gap"]},
    {"id": "h06", "args": [[[1, 2], [1, 3], [1, 1]]], "tags": ["tie-by-index"]},
    {"id": "h07", "args": [[[3, 1], [2, 1], [1, 1], [0, 1]]], "tags": ["reverse-order"]},
    {"id": "h08", "args": [[[0, 5], [1, 1], [2, 1], [3, 1]]], "tags": ["convoy"]},
    {"id": "h09", "args": [[[0, 1], [5, 1], [5, 1]]], "tags": ["idle-gap", "tie-by-index"]},
    {"id": "h10", "args": [[[4, 4], [0, 1], [4, 1]]], "tags": ["tie-by-index", "out-of-order"]},
    {"id": "h11", "args": [[[0, 10]]], "tags": ["edge", "single"]},
    {"id": "h12", "args": [[[7, 3], [0, 2], [3, 6], [3, 1]]], "tags": ["mixed"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        count = (x >> 8) % 8
        jobs = []
        for _r in range(count):
            x = _next(x)
            arrival = (x >> 8) % 11
            x = _next(x)
            burst = (x >> 8) % 8 + 1
            jobs.append([arrival, burst])
        out.append([jobs])
    return out


for _i, _a in enumerate(_lcg(853, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
