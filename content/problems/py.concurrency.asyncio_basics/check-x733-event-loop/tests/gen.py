"""Inputs of check-x733-event-loop; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[0, 2], [1, 3]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[[4, 9]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[1, 1], [2, 1], [3, 1], [4, 1]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[0, 2], [1, 3]]], "tags": []},
    {"id": "h05", "args": [[[5, 1], [6, 1], [7, 2]]], "tags": []},
    {"id": "h06", "args": [[[9, 3], [8, 1], [7, 3]]], "tags": []},
    {"id": "h07", "args": [[[0, 1], [1, 5]]], "tags": []},
    {
        "id": "h08",
        "args": [[[i, 1 + i % 3] for i in range(12)]],
        "tags": [],
    },
    {"id": "h09", "args": [[[2, 4], [1, 4], [0, 4]]], "tags": []},
    {"id": "h10", "args": [[[10, 1]]], "tags": ["edge"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_tasks = (x >> 8) % 9
        tasks = []
        for i in range(n_tasks):
            x = (x * 1103515245 + 12345) % 2147483648
            tasks.append([i, 1 + (x >> 8) % 5])
        out.append([tasks])
    return out


for _i, _a in enumerate(_lcg(13, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
