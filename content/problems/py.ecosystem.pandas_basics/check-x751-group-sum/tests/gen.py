"""Inputs of check-x751-group-sum; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["a", 3], ["b", 2], ["a", 5]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["a", 4]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["pear", 2], ["fig", 2], ["kiwi", 2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", 0], ["b", 0]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["x", 1], ["x", 1], ["x", 1]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["b", 3], ["a", 1], ["a", 2], ["c", 1]]], "tags": ["edge"]},
    {"id": "h07", "args": [[["x", -5], ["y", 7], ["x", 3], ["y", -7]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["o'brien", 2], ["a;b", 3], ["o'brien", 1]]], "tags": ["edge"]},
    {"id": "h09", "args": [[["m", 0], ["m", 4], ["n", 4]]], "tags": []},
    {
        "id": "h10",
        "args": [[["p9", 9], ["p8", 8], ["p3", 7], ["p4", 6], ["p1", 5], ["p6", 4], ["p1", 1]]],
        "tags": ["many_keys"],
    },
]

_POOL = ["apple", "banana", "cherry", "date", "elder", "fig", "grape", "honey"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rows = (x >> 8) % 12
        rows = []
        for _r in range(n_rows):
            x = (x * 1103515245 + 12345) % 2147483648
            key = _POOL[(x >> 8) % len(_POOL)]
            x = (x * 1103515245 + 12345) % 2147483648
            value = (x >> 8) % 21 - 10
            rows.append([key, value])
        out.append([rows])
    return out


for _i, _a in enumerate(_lcg(29, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
