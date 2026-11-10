"""Inputs of check-x868-live-inodes; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["create", "a"], ["link", "b", "a"], ["unlink", "a"]]]},
    {"id": "s2", "args": [[["create", "a"], ["unlink", "a"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[["create", "a"], ["unlink", "a"]]], "tags": ["freed"]},
    {
        "id": "h03",
        "args": [[["create", "a"], ["link", "b", "a"], ["unlink", "a"]]],
        "tags": ["hard-link-alive"],
    },
    {
        "id": "h04",
        "args": [[["create", "a"], ["link", "b", "a"], ["unlink", "a"], ["unlink", "b"]]],
        "tags": ["all-links-removed"],
    },
    {"id": "h05", "args": [[["link", "b", "a"], ["create", "a"]]], "tags": ["link-absent"]},
    {"id": "h06", "args": [[["unlink", "x"], ["create", "a"]]], "tags": ["unlink-absent"]},
    {
        "id": "h07",
        "args": [
            [
                ["create", "a"],
                ["create", "b"],
                ["link", "c", "a"],
                ["unlink", "a"],
                ["unlink", "b"],
            ]
        ],
        "tags": ["multi-inode"],
    },
    {
        "id": "h08",
        "args": [[["create", "a"], ["unlink", "a"], ["create", "a"]]],
        "tags": ["recreate"],
    },
    {
        "id": "h09",
        "args": [[["create", "a"], ["unlink", "a"], ["create", "a"], ["unlink", "a"]]],
        "tags": ["recreate", "freed"],
    },
    {
        "id": "h10",
        "args": [[["create", "a"], ["link", "b", "a"], ["link", "c", "b"], ["unlink", "a"]]],
        "tags": ["chain-link"],
    },
    {
        "id": "h11",
        "args": [[["create", "a"], ["create", "b"], ["create", "c"]]],
        "tags": ["only-create"],
    },
    {
        "id": "h12",
        "args": [[["create", "a"], ["unlink", "a"], ["link", "b", "a"], ["unlink", "a"]]],
        "tags": ["link-after-free"],
    },
]

_NAMES = ["a", "b", "c", "d"]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        m = (x >> 8) % 14
        ops = []
        for _i in range(m):
            x = _next(x)
            kind = (x >> 8) % 3
            x = _next(x)
            n1 = _NAMES[(x >> 8) % 4]
            if kind == 0:
                ops.append(["create", n1])
            elif kind == 1:
                x = _next(x)
                n2 = _NAMES[(x >> 8) % 4]
                ops.append(["link", n1, n2])
            else:
                ops.append(["unlink", n1])
        out.append([ops])
    return out


for _i, _a in enumerate(_lcg(868, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
