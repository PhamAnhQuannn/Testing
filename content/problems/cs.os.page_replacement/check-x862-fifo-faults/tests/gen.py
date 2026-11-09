"""Inputs of check-x862-fifo-faults; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3]},
    {"id": "s2", "args": [[7, 0, 1, 2, 0, 3, 0, 4], 3]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[1, 2, 1, 2, 3, 3, 1], 1], "tags": ["one-frame"]},
    {"id": "h03", "args": [[5, 5, 5, 5, 5], 2], "tags": ["all-same"]},
    {"id": "h04", "args": [[1, 2, 3, 1, 2, 3, 1], 3], "tags": ["no-eviction"]},
    {"id": "h05", "args": [[1, 2, 3], 10], "tags": ["no-eviction", "many-frames"]},
    {
        "id": "h06",
        "args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4],
        "tags": ["belady", "more-frames"],
    },
    {
        "id": "h07",
        "args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3],
        "tags": ["belady", "fewer-frames"],
    },
    {"id": "h08", "args": [[1, 2, 3, 4, 5, 6], 2], "tags": ["all-distinct"]},
    {"id": "h09", "args": [[1, 2, 3, 1, 2, 3, 1, 2, 3], 2], "tags": ["cyclic", "thrash"]},
    {"id": "h10", "args": [[1, 2, 1, 3, 2], 2], "tags": ["small"]},
    {"id": "h11", "args": [[3, 3, 1, 1, 2, 2, 3, 3], 2], "tags": ["repeated-access"]},
    {"id": "h12", "args": [[10, 20, 30, 10, 40, 20, 50, 10], 3], "tags": ["large-pids"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        length = (x >> 8) % 15
        refs = []
        for _k in range(length):
            x = _next(x)
            refs.append(1 + (x >> 8) % 5)
        x = _next(x)
        frames = 1 + (x >> 8) % 4
        out.append([refs, frames])
    return out


for _i, _a in enumerate(_lcg(862, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
