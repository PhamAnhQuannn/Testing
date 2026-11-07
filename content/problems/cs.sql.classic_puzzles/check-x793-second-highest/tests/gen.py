"""Inputs of check-x793-second-highest; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["an", 9], ["binh", 7], ["chi", 9], ["dung", 7]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["solo", 5]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["a", 4], ["b", 4], ["c", 4]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", 10], ["b", 3]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["a", 8], ["b", 8], ["c", 6], ["d", 6], ["e", 6]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["a", -1], ["b", -5], ["c", -3]]], "tags": ["edge"]},
    {"id": "h07", "args": [[["o'brien", 2], ["a;b", 5], ["z", 2]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["x", 0], ["y", 7], ["z", 0]]], "tags": ["edge"]},
    {"id": "h09", "args": [[["m", 1], ["n", 2], ["o", 3], ["p", 4], ["q", 5]]], "tags": []},
    {"id": "h10", "args": [[["b", 9], ["a", 9], ["d", 5], ["c", 5], ["e", 2]]], "tags": ["edge"]},
]

_POOL = ["an", "binh", "chi", "dung", "em", "giang", "ha", "khoa"]


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
            score = (x >> 8) % 7 - 3
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
