"""Inputs of check-x722-counter; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["R", 0], ["R", 1], ["W", 0], ["W", 1]]]},
    {"id": "s2", "args": [[["R", 0], ["W", 0], ["R", 1], ["W", 1]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["R", 0], ["R", 1], ["W", 1], ["W", 0]]], "tags": ["edge"]},
    {
        "id": "h03",
        "args": [[["R", 0], ["W", 0], ["R", 0], ["W", 0], ["R", 0], ["W", 0]]],
        "tags": [],
    },
    {"id": "h04", "args": [[["W", 3]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["R", 7]]], "tags": ["edge"]},
    {
        "id": "h06",
        "args": [[["R", 0], ["R", 1], ["R", 2], ["W", 0], ["W", 1], ["W", 2]]],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "args": [[["R", 0], ["R", 1], ["W", 0], ["R", 0], ["W", 0], ["W", 1]]],
        "tags": [],
    },
    {
        "id": "h08",
        "args": [[["R", 0], ["W", 0], ["R", 1], ["W", 1], ["R", 2], ["W", 2]]],
        "tags": [],
    },
    {"id": "h09", "args": [[["R", 1], ["W", 0], ["W", 1], ["R", 0], ["W", 0]]], "tags": []},
    {"id": "h10", "args": [[["W", 0], ["W", 0], ["W", 1]]], "tags": ["edge"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 13
        sched = []
        for _k in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            action = "R" if (x >> 8) % 2 == 0 else "W"
            x = (x * 1103515245 + 12345) % 2147483648
            tid = (x >> 8) % 3
            sched.append([action, tid])
        out.append([sched])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
