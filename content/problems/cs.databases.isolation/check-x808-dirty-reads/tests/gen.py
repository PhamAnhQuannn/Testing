"""Inputs of check-x808-dirty-reads; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [[["write", "T1", "x", 5], ["read", "T2", "x"], ["abort", "T1"]]],
    },
    {
        "id": "s2",
        "args": [[["write", "T1", "x", 5], ["read", "T2", "x"], ["commit", "T1"]]],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {
        "id": "h02",
        "args": [[["write", "T1", "x", 1], ["commit", "T1"], ["read", "T2", "x"], ["abort", "T1"]]],
        "tags": ["edge", "read-committed"],
    },
    {
        "id": "h03",
        "args": [[["write", "T1", "x", 1], ["read", "T2", "x"], ["abort", "T1"]]],
        "tags": ["dirty"],
    },
    {
        "id": "h04",
        "args": [[["write", "T1", "x", 1], ["read", "T1", "x"], ["abort", "T1"]]],
        "tags": ["edge", "self-read"],
    },
    {
        "id": "h05",
        "args": [
            [
                ["write", "T1", "x", 1],
                ["write", "T1", "y", 2],
                ["read", "T3", "x"],
                ["read", "T2", "y"],
                ["abort", "T1"],
            ]
        ],
        "tags": ["dirty", "multiple-readers"],
    },
    {
        "id": "h06",
        "args": [[["write", "T1", "x", 1], ["read", "T2", "x"], ["commit", "T1"]]],
        "tags": ["commit"],
    },
    {
        "id": "h07",
        "args": [[["write", "T1", "x", 1], ["read", "T2", "x"], ["commit", "T1"], ["abort", "T3"]]],
        "tags": ["commit", "abort-other"],
    },
    {
        "id": "h08",
        "args": [
            [["write", "T1", "x", 1], ["write", "T2", "x", 2], ["read", "T3", "x"], ["abort", "T1"]]
        ],
        "tags": ["rewrite", "writer-overwritten"],
    },
    {
        "id": "h09",
        "args": [
            [["write", "T1", "x", 1], ["write", "T2", "x", 2], ["read", "T3", "x"], ["abort", "T2"]]
        ],
        "tags": ["rewrite", "dirty"],
    },
    {
        "id": "h10",
        "args": [[["read", "T2", "x"], ["write", "T1", "x", 1], ["abort", "T1"]]],
        "tags": ["read-before-write"],
    },
    {
        "id": "h11",
        "args": [[["write", "T1", "x", 1], ["abort", "T1"], ["read", "T2", "x"]]],
        "tags": ["read-after-abort"],
    },
    {
        "id": "h12",
        "args": [
            [
                ["write", "T1", "x", 1],
                ["write", "T2", "y", 2],
                ["read", "T3", "x"],
                ["read", "T3", "y"],
                ["commit", "T1"],
                ["abort", "T2"],
            ]
        ],
        "tags": ["dirty", "two-writers"],
    },
]

TXNS = ["T1", "T2", "T3"]
KEYS = ["x", "y"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 11
        ops = []
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            pick = (x >> 8) % 10
            x = (x * 1103515245 + 12345) % 2147483648
            txn = TXNS[(x >> 8) % len(TXNS)]
            x = (x * 1103515245 + 12345) % 2147483648
            key = KEYS[(x >> 8) % len(KEYS)]
            if pick < 4:
                x = (x * 1103515245 + 12345) % 2147483648
                ops.append(["write", txn, key, (x >> 8) % 19 - 9])
            elif pick < 7:
                ops.append(["read", txn, key])
            elif pick < 9:
                ops.append(["commit", txn])
            else:
                ops.append(["abort", txn])
        out.append([ops])
    return out


for _i, _a in enumerate(_lcg(31, 12)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
