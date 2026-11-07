"""Inputs of check-x784-above-average; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["an", 3], ["binh", 9], ["chi", 6]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["solo", 5]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["a", 2], ["b", 2], ["c", 2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", 1], ["b", 9], ["c", 9], ["d", 1]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["a", -5], ["b", -1], ["c", -3]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["x", 0], ["y", 0], ["z", 4]]], "tags": ["edge"]},
    {"id": "h07", "args": [[["o'brien", 8], ["a;b", 2], ["z", 8]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["m", 10], ["n", 7], ["p", 7], ["q", 1]]], "tags": []},
    {"id": "h09", "args": [[["b", 3], ["a", 3], ["c", 0]]], "tags": ["edge"]},
    {"id": "h10", "args": [[["a", -2], ["b", 0], ["c", 5], ["d", 5], ["e", -9]]], "tags": []},
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
            name = _POOL[(x >> 8) % len(_POOL)]
            x = (x * 1103515245 + 12345) % 2147483648
            score = (x >> 8) % 21 - 10
            rows.append([name, score])
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
