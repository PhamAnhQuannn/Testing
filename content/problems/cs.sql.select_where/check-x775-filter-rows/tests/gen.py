"""Inputs of check-x775-filter-rows; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["an", 8, 1], ["binh", 9, 0], ["chi", 8, 1]], 8]},
    {"id": "s2", "args": [[], 5]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 0], "tags": ["edge"]},
    {"id": "h02", "args": [[["an", 4, 1], ["binh", 3, 1]], 10], "tags": ["edge"]},
    {"id": "h03", "args": [[["an", 9, 0], ["binh", 8, 0], ["chi", 7, 0]], 0], "tags": ["edge"]},
    {"id": "h04", "args": [[["b", 5, 1], ["a", 5, 1], ["c", 5, 1]], 5], "tags": ["edge"]},
    {"id": "h05", "args": [[["an", 6, 1], ["binh", 7, 1]], -100], "tags": ["edge"]},
    {"id": "h06", "args": [[["an", 6, 1], ["binh", 7, 1]], 100], "tags": ["edge"]},
    {"id": "h07", "args": [[["o'brien", 7, 1], ["a;b", 7, 1], ["x", 2, 1]], 7], "tags": ["edge"]},
    {"id": "h08", "args": [[["m", 3, 1], ["n", 9, 1], ["p", 6, 0], ["q", 6, 1]], 4], "tags": []},
    {"id": "h09", "args": [[["x", 0, 1], ["y", 0, 0]], 0], "tags": ["edge"]},
    {
        "id": "h10",
        "args": [
            [["p1", 9, 1], ["p2", 8, 1], ["p3", 7, 0], ["p4", 6, 1], ["p5", 5, 1], ["p1", 9, 1]],
            6,
        ],
        "tags": [],
    },
]

_POOL = ["an", "binh", "chi", "dung", "em", "phuc", "giang", "hoa"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rows = (x >> 8) % 12
        x = (x * 1103515245 + 12345) % 2147483648
        threshold = (x >> 8) % 11
        rows = []
        for _r in range(n_rows):
            x = (x * 1103515245 + 12345) % 2147483648
            name = _POOL[(x >> 8) % len(_POOL)]
            x = (x * 1103515245 + 12345) % 2147483648
            score = (x >> 8) % 11
            x = (x * 1103515245 + 12345) % 2147483648
            active = (x >> 8) % 2
            rows.append([name, score, active])
        out.append([rows, threshold])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
