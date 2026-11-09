"""Inputs of check-x865-select-ready; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[5, 3, 8, 3], [8, 3, 9]]},
    {"id": "s2", "args": [[1, 2, 3], [2]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[], [1, 2]], "tags": ["edge", "empty-fds"]},
    {"id": "h03", "args": [[1, 2, 3], []], "tags": ["edge", "none-ready"]},
    {"id": "h04", "args": [[1, 2, 3], [4, 5, 6]], "tags": ["no-overlap"]},
    {"id": "h05", "args": [[4, 6, 8], [8, 4, 6]], "tags": ["all-overlap"]},
    {"id": "h06", "args": [[3, 3, 3, 5, 5], [3, 5]], "tags": ["duplicates"]},
    {"id": "h07", "args": [[2, 4], [1, 2, 3, 4, 5, 9]], "tags": ["ready-superset"]},
    {"id": "h08", "args": [[1, 2, 3, 4], [2, 4, 4, 4]], "tags": ["duplicates-in-ready"]},
    {"id": "h09", "args": [[1, 2, 3, 4, 5], [1, 3, 5]], "tags": ["already-sorted"]},
    {"id": "h10", "args": [[9, 7, 5, 3, 1], [1, 5, 9]], "tags": ["reverse-sorted"]},
    {"id": "h11", "args": [[7], [7]], "tags": ["edge", "single"]},
    {"id": "h12", "args": [[7], [8]], "tags": ["edge", "single", "no-overlap"]},
    {"id": "h13", "args": [[0, 10, 1000], [1000, 0]], "tags": ["large-fds"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        n_fds = (x >> 8) % 9
        fds = []
        for _i in range(n_fds):
            x = _next(x)
            fds.append((x >> 8) % 10)
        x = _next(x)
        n_ready = (x >> 8) % 9
        ready = []
        for _i in range(n_ready):
            x = _next(x)
            ready.append((x >> 8) % 12)
        out.append([fds, ready])
    return out


for _i, _a in enumerate(_lcg(47, 10)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
