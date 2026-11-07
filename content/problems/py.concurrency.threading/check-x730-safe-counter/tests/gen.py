"""Inputs of check-x730-safe-counter; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [[["acq", 0], ["inc", 0], ["inc", 0], ["rel", 0], ["acq", 1], ["inc", 1]]],
    },
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[["inc", 0], ["inc", 1]]], "tags": ["edge"]},
    {
        "id": "h02",
        "args": [[["acq", 0], ["acq", 1], ["inc", 1], ["rel", 0], ["inc", 0]]],
        "tags": ["edge"],
    },
    {"id": "h03", "args": [[["acq", 0], ["rel", 1], ["inc", 0], ["inc", 0]]], "tags": ["edge"]},
    {"id": "h04", "args": [[]], "tags": ["edge"]},
    {"id": "h05", "args": [[["acq", 2], ["inc", 2], ["rel", 2]]], "tags": ["edge"]},
    {
        "id": "h06",
        "args": [
            [["acq", 0], ["inc", 0], ["acq", 1], ["inc", 1], ["rel", 0], ["acq", 1], ["inc", 1]]
        ],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [[["acq", 0], ["acq", 0], ["inc", 0], ["rel", 0], ["rel", 0], ["inc", 0]]],
        "tags": ["edge"],
    },
    {
        "id": "h08",
        "args": [
            [
                ["acq", 0],
                ["inc", 0],
                ["rel", 0],
                ["acq", 1],
                ["inc", 1],
                ["inc", 1],
                ["rel", 1],
                ["acq", 2],
                ["inc", 2],
                ["rel", 2],
            ]
        ],
        "tags": [],
    },
    {
        "id": "h09",
        "args": [[["rel", 0], ["acq", 3], ["inc", 3], ["inc", 0], ["rel", 3]]],
        "tags": [],
    },
    {
        "id": "h10",
        "args": [
            [["acq", 1], ["inc", 0], ["inc", 1], ["rel", 0], ["inc", 1], ["rel", 1], ["inc", 1]]
        ],
        "tags": [],
    },
]

_OPS = ["acq", "inc", "rel"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 16
        ops = []
        for _i in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            op = _OPS[(x >> 8) % 3]
            x = (x * 1103515245 + 12345) % 2147483648
            tid = (x >> 8) % 3
            ops.append([op, tid])
        out.append([ops])
    return out


for _i, _a in enumerate(_lcg(13, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
