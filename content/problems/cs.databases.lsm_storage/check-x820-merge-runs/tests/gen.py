"""Inputs of check-x820-merge-runs; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [[[["a", 1], ["b", 2]], [["b", 9], ["c", 3]]]],
    },
    {
        "id": "s2",
        "args": [[[["x", 5]], [["y", -1]], [["x", 7]]]],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[[], [], []]], "tags": ["edge", "all-empty"]},
    {"id": "h03", "args": [[[["b", 2], ["a", 1]]]], "tags": ["edge", "single-run", "sorted"]},
    {
        "id": "h04",
        "args": [[[["a", 1], ["c", 3]], [["b", 2], ["d", 4]]]],
        "tags": ["disjoint"],
    },
    {
        "id": "h05",
        "args": [[[["a", 1], ["b", 2]], [["a", 8], ["b", 9]]]],
        "tags": ["full-overlap", "newest-wins"],
    },
    {
        "id": "h06",
        "args": [[[["a", 1], ["b", 1]], [["a", 2], ["c", 2]], [["a", 3], ["b", 3], ["d", 3]]]],
        "tags": ["three-runs", "layering"],
    },
    {
        "id": "h07",
        "args": [[[['k"1', 1], ["it's", 2]], [['k"1', 5]]]],
        "tags": ["quotes"],
    },
    {
        "id": "h08",
        "args": [[[["a", -5], ["b", 0]], [["b", -7]]]],
        "tags": ["negative"],
    },
    {
        "id": "h09",
        "args": [[[["a", 1]], [], [["b", 2]]]],
        "tags": ["empty-run-among"],
    },
    {
        "id": "h10",
        "args": [[[], [["z", 1], ["a", 2]], []]],
        "tags": ["empty-run-among", "sorted"],
    },
    {
        "id": "h11",
        "args": [[[["a", 1]], [["a", 2]], [["a", 3]], [["a", 4]]]],
        "tags": ["same-key", "newest-wins"],
    },
]

KEYS = ["a", "b", "c", "d", "e", "f"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        nruns = (x >> 8) % 5
        runs = []
        for _r in range(nruns):
            x = (x * 1103515245 + 12345) % 2147483648
            size = (x >> 8) % 5
            used = []
            run = []
            for _p in range(size):
                x = (x * 1103515245 + 12345) % 2147483648
                key = KEYS[(x >> 8) % len(KEYS)]
                x = (x * 1103515245 + 12345) % 2147483648
                if key not in used:
                    used.append(key)
                    run.append([key, (x >> 8) % 19 - 9])
            runs.append(run)
        out.append([runs])
    return out


for _i, _a in enumerate(_lcg(31, 10)):
    HIDDEN.append({"id": f"h{12 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
