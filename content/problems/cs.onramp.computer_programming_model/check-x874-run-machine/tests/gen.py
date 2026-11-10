"""Inputs of check-x874-run-machine; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["set", "x", 5], ["set", "y", 3], ["add", "x", "y"], ["out", "x"]]]},
    {"id": "s2", "args": [[["out", "z"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[["out", "z"]]], "tags": ["unset-read"]},
    {
        "id": "h03",
        "args": [[["set", "x", 5], ["set", "y", 3], ["add", "x", "y"], ["out", "x"]]],
        "tags": ["add"],
    },
    {
        "id": "h04",
        "args": [[["set", "a", 10], ["set", "b", 4], ["sub", "a", "b"], ["out", "a"]]],
        "tags": ["sub"],
    },
    {"id": "h05", "args": [[["add", "x", "y"], ["out", "x"]]], "tags": ["unset-add"]},
    {"id": "h06", "args": [[["sub", "x", "y"], ["out", "x"], ["out", "y"]]], "tags": ["unset-sub"]},
    {
        "id": "h07",
        "args": [[["set", "x", 1], ["out", "x"], ["set", "x", 2], ["out", "x"], ["out", "x"]]],
        "tags": ["multi-out", "overwrite"],
    },
    {
        "id": "h08",
        "args": [[["set", "x", 3], ["add", "x", "x"], ["add", "x", "x"], ["out", "x"]]],
        "tags": ["self-add"],
    },
    {
        "id": "h09",
        "args": [[["set", "x", 7], ["sub", "x", "x"], ["out", "x"]]],
        "tags": ["self-sub"],
    },
    {
        "id": "h10",
        "args": [
            [["set", "a", 2], ["set", "b", -5], ["add", "a", "b"], ["out", "a"], ["out", "b"]]
        ],
        "tags": ["negative"],
    },
    {
        "id": "h11",
        "args": [
            [
                ["set", "a", 1],
                ["set", "b", 1],
                ["add", "a", "b"],
                ["add", "b", "a"],
                ["add", "a", "b"],
                ["out", "a"],
                ["out", "b"],
            ]
        ],
        "tags": ["fibonacci"],
    },
    {
        "id": "h12",
        "args": [[["set", "x", 0], ["out", "x"], ["set", "y", 9], ["out", "y"], ["out", "x"]]],
        "tags": ["zero"],
    },
]

_VARS = ["a", "b", "c", "d"]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        m = (x >> 8) % 14
        prog = []
        for _i in range(m):
            x = _next(x)
            kind = (x >> 8) % 4
            x = _next(x)
            v1 = _VARS[(x >> 8) % 4]
            if kind == 0:
                x = _next(x)
                prog.append(["set", v1, (x >> 8) % 41 - 20])
            elif kind in (1, 2):
                x = _next(x)
                v2 = _VARS[(x >> 8) % 4]
                prog.append(["add" if kind == 1 else "sub", v1, v2])
            else:
                prog.append(["out", v1])
        out.append([prog])
    return out


for _i, _a in enumerate(_lcg(874, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
