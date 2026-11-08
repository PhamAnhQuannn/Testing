"""Inputs of check-x811-snapshot-reads; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[10, 100], [20, 200], [30, 300]], [25, 10, 5, 30]]},
    {"id": "s2", "args": [[[3, -7]], [2, 3, 4]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [1, 2, 3]], "tags": ["edge", "empty-versions"]},
    {"id": "h02", "args": [[[5, 1], [9, 2]], []], "tags": ["edge", "empty-reads"]},
    {"id": "h03", "args": [[], []], "tags": ["edge", "empty"]},
    {"id": "h04", "args": [[[10, 1], [20, 2]], [0, 9, -5]], "tags": ["edge", "before-first"]},
    {"id": "h05", "args": [[[10, 1], [20, 2], [30, 3]], [10, 20, 30]], "tags": ["exact-ts"]},
    {"id": "h06", "args": [[[10, 1], [20, 2], [30, 3]], [31, 100, 30]], "tags": ["after-last"]},
    {"id": "h07", "args": [[[7, 42]], [6, 7, 8]], "tags": ["single-version"]},
    {"id": "h08", "args": [[[1, -5], [4, -9], [8, 0]], [1, 3, 4, 7, 8]], "tags": ["negative"]},
    {
        "id": "h09",
        "args": [[[-10, 5], [0, 6], [10, 7]], [-11, -10, -1, 0, 9, 10]],
        "tags": ["neg-ts"],
    },
    {"id": "h10", "args": [[[10, 1], [20, 2]], [15, 15, 25, 5, 15]], "tags": ["repeat-reads"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        nv = (x >> 8) % 7
        x = (x * 1103515245 + 12345) % 2147483648
        ts = (x >> 8) % 7 - 3
        versions = []
        for _r in range(nv):
            x = (x * 1103515245 + 12345) % 2147483648
            ts += 1 + (x >> 8) % 5
            x = (x * 1103515245 + 12345) % 2147483648
            versions.append([ts, (x >> 8) % 41 - 20])
        last = ts
        x = (x * 1103515245 + 12345) % 2147483648
        nr = (x >> 8) % 9
        reads = []
        for _r in range(nr):
            x = (x * 1103515245 + 12345) % 2147483648
            reads.append((x >> 8) % (last + 12) - 5)
        out.append([versions, reads])
    return out


for _i, _a in enumerate(_lcg(37, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
