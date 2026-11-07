"""Inputs of check-x805-apply-tx; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [
            [
                ["set", "a", 1],
                ["begin"],
                ["set", "a", 9],
                ["set", "b", 2],
                ["rollback"],
                ["set", "c", 3],
            ]
        ],
    },
    {
        "id": "s2",
        "args": [[["begin"], ["set", "x", 5], ["commit"], ["set", "y", -1]]],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {
        "id": "h02",
        "args": [[["begin"], ["set", "a", 1], ["rollback"]]],
        "tags": ["edge", "rollback"],
    },
    {
        "id": "h03",
        "args": [[["begin"], ["set", "a", 1], ["commit"]]],
        "tags": ["edge", "commit"],
    },
    {"id": "h04", "args": [[["begin"], ["commit"]]], "tags": ["edge", "empty-tx"]},
    {
        "id": "h05",
        "args": [[["rollback"], ["set", "a", 2], ["rollback"]]],
        "tags": ["edge", "no-tx-noop"],
    },
    {
        "id": "h06",
        "args": [[["set", "a", 1], ["commit"], ["set", "b", 2]]],
        "tags": ["edge", "no-tx-noop"],
    },
    {
        "id": "h07",
        "args": [[["begin"], ["set", "a", 1], ["begin"], ["set", "b", 2], ["commit"]]],
        "tags": ["edge", "begin-in-tx"],
    },
    {
        "id": "h08",
        "args": [[["set", "a", 1], ["begin"], ["set", "a", 2], ["set", "a", 3], ["commit"]]],
        "tags": ["overwrite", "commit"],
    },
    {
        "id": "h09",
        "args": [[["set", "b", 5], ["set", "a", 4], ["set", "b", -5]]],
        "tags": ["outside-tx", "sorted"],
    },
    {
        "id": "h10",
        "args": [
            [["set", "a", 1], ["begin"], ["set", "a", 2], ["rollback"], ["begin"], ["set", "c", 7]]
        ],
        "tags": ["open-at-end"],
    },
    {
        "id": "h11",
        "args": [
            [["begin"], ["set", "a", 1], ["commit"], ["begin"], ["set", "a", 2], ["rollback"]]
        ],
        "tags": ["rollback", "commit"],
    },
]

KEYS = ["a", "b", "c", "d"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 13
        ops = []
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            pick = (x >> 8) % 10
            if pick < 5:
                x = (x * 1103515245 + 12345) % 2147483648
                key = KEYS[(x >> 8) % len(KEYS)]
                x = (x * 1103515245 + 12345) % 2147483648
                ops.append(["set", key, (x >> 8) % 19 - 9])
            elif pick < 7:
                ops.append(["begin"])
            elif pick < 9:
                ops.append(["commit"])
            else:
                ops.append(["rollback"])
        out.append([ops])
    return out


for _i, _a in enumerate(_lcg(29, 10)):
    HIDDEN.append({"id": f"h{12 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
