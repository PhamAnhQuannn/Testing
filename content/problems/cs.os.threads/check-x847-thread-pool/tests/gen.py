"""Inputs of check-x847-thread-pool; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[3, 1, 2, 4], 2]},
    {"id": "s2", "args": [[], 3]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 1], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[5], 1], "tags": ["edge", "single"]},
    {"id": "h03", "args": [[4, 2, 7, 1], 1], "tags": ["single-worker"]},
    {"id": "h04", "args": [[2, 3], 5], "tags": ["workers-gt-tasks"]},
    {"id": "h05", "args": [[2, 2, 2, 2, 2, 2], 3], "tags": ["all-equal"]},
    {"id": "h06", "args": [[1, 1, 1, 1, 1], 2], "tags": ["tie-breaking", "all-equal"]},
    {"id": "h07", "args": [[3, 1, 2, 4], 2], "tags": ["tie-breaking"]},
    {"id": "h08", "args": [[10, 1, 1, 1, 1], 3], "tags": ["one-big-task"]},
    {"id": "h09", "args": [[1, 1, 1, 10], 2], "tags": ["one-big-task"]},
    {"id": "h10", "args": [[0, 0, 5, 0], 2], "tags": ["zero-duration"]},
    {"id": "h11", "args": [[5, 5, 3, 3, 1], 4], "tags": ["tie-breaking"]},
    {"id": "h12", "args": [[6, 4, 3, 3, 2, 2, 1], 3], "tags": ["mixed"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        count = (x >> 8) % 9
        tasks = []
        for _r in range(count):
            x = _next(x)
            tasks.append((x >> 8) % 10)
        x = _next(x)
        workers = (x >> 8) % 4 + 1
        out.append([tasks, workers])
    return out


for _i, _a in enumerate(_lcg(47, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
