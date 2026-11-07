"""Inputs of check-x772-select-all; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["an", 8], ["binh", 5], ["chi", 8]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["an", 4]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["pear", 2], ["fig", 2], ["kiwi", 2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["an", 0], ["binh", 0]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["an", -1], ["binh", -5], ["chi", 0], ["dung", -1]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["b", 3], ["a", 1], ["a", 2], ["c", 1]]], "tags": ["edge"]},
    {"id": "h07", "args": [[["x", 5], ["y", 7], ["z", 6], ["x", 3]]], "tags": []},
    {"id": "h08", "args": [[["o'brien", 2], ["a;b", 3], ["o'brien", 1]]], "tags": ["edge"]},
    {"id": "h09", "args": [[["m", 4], ["m", 4], ["n", 4]]], "tags": ["edge"]},
    {
        "id": "h10",
        "args": [[["p1", 9], ["p2", 8], ["p3", 7], ["p4", 6], ["p5", 5], ["p6", 4], ["p7", 9]]],
        "tags": [],
    },
]

_POOL = ["an", "binh", "chi", "dung", "em", "ha", "khoa", "lan"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rows = (x >> 8) % 12
        rows = []
        for _r in range(n_rows):
            x = (x * 1103515245 + 12345) % 2147483648
            name = _POOL[(x >> 8) % len(_POOL)]
            x = (x * 1103515245 + 12345) % 2147483648
            score = (x >> 8) % 11 - 3
            rows.append([name, score])
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
