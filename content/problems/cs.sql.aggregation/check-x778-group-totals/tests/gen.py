"""Inputs of check-x778-group-totals; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["a", 3], ["b", 5], ["a", 4], ["b", -5]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["apple", 4]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["a", 2], ["a", 2], ["a", 2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", 3], ["a", -3], ["b", 1]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["a", -1], ["b", -2]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["pear", 2], ["fig", 2], ["kiwi", 2]]], "tags": ["edge"]},
    {"id": "h07", "args": [[["x", 0], ["y", 0]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["o'brien", 2], ["a;b", 3], ["o'brien", 1]]], "tags": ["edge"]},
    {"id": "h09", "args": [[["m", 5], ["m", -2], ["n", 3], ["n", 1], ["z", -9]]], "tags": []},
    {"id": "h10", "args": [[["b", 4], ["a", 1], ["a", 3], ["c", 4]]], "tags": ["edge"]},
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
            category = _POOL[(x >> 8) % len(_POOL)]
            x = (x * 1103515245 + 12345) % 2147483648
            amount = (x >> 8) % 11 - 5
            rows.append([category, amount])
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
