"""Inputs of check-x754-pivot-sum; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["a", "x", 2], ["a", "y", 3], ["a", "x", 5]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["a", "x", 4]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["a", "x", 1], ["a", "x", 1], ["a", "x", 1]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", "x", 0], ["b", "y", 0]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["a", "x", 5], ["a", "x", -5], ["b", "x", -3]]], "tags": ["edge"]},
    {
        "id": "h06",
        "args": [[["a", "x", 1], ["a", "y", 2], ["b", "x", 3], ["b", "y", 4], ["a", "x", 10]]],
        "tags": [],
    },
    {"id": "h07", "args": [[["o'brien", "a;b", 2], ["o'brien", "a;b", 3]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["r1", "c1", 1], ["r2", "c1", 2], ["r3", "c1", 3]]], "tags": []},
    {"id": "h09", "args": [[["r", "c1", 1], ["r", "c2", 2], ["r", "c3", 3]]], "tags": []},
    {"id": "h10", "args": [[["", "", 7], ["", "x", 1], ["", "", -2]]], "tags": ["edge"]},
]

_ROWS = ["a", "b", "c", "d"]
_COLS = ["x", "y", "z"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rows = (x >> 8) % 12
        rows = []
        for _r in range(n_rows):
            x = (x * 1103515245 + 12345) % 2147483648
            r = _ROWS[(x >> 8) % len(_ROWS)]
            x = (x * 1103515245 + 12345) % 2147483648
            c = _COLS[(x >> 8) % len(_COLS)]
            x = (x * 1103515245 + 12345) % 2147483648
            v = (x >> 8) % 21 - 10
            rows.append([r, c, v])
        out.append([rows])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
