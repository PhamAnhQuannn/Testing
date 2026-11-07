"""Inputs of check-x796-is-candidate-key; `expected` comes from solution.py via gen_hidden."""


def _r(i, g):
    return {"id": i, "g": g}


SAMPLES = [
    {
        "id": "s1",
        "args": [[_r(1, "a"), _r(2, "a"), _r(1, "b")], ["id"]],
    },
    {
        "id": "s2",
        "args": [[_r(1, "a"), _r(2, "a"), _r(1, "b")], ["id", "g"]],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[], ["id"]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[_r(1, "a")], ["id"]], "tags": ["edge", "single"]},
    {"id": "h03", "args": [[_r(1, "a"), _r(None, "b")], ["id"]], "tags": ["edge", "null"]},
    {"id": "h04", "args": [[_r(1, "a"), _r(1, "a")], ["id", "g"]], "tags": ["edge", "duplicate"]},
    {
        "id": "h05",
        "args": [[_r(1, "a"), _r(1, "b"), _r(2, "a")], ["id", "g"]],
        "tags": ["multi-col", "unique"],
    },
    {"id": "h06", "args": [[_r(1, "a"), _r(2, "a")], ["g"]], "tags": ["non-unique"]},
    {"id": "h07", "args": [[_r(1, "a"), _r(2, "b"), _r(3, "c")], ["id"]], "tags": ["distinct"]},
    {"id": "h08", "args": [[_r(1, "a"), _r(2, None)], ["g"]], "tags": ["edge", "null"]},
    {"id": "h09", "args": [[_r(1, None), _r(2, "a")], ["id"]], "tags": ["null-other-col"]},
    {"id": "h10", "args": [[_r(1, "a"), _r(2, "b"), _r(1, "c")], ["id"]], "tags": ["non-unique"]},
    {"id": "h11", "args": [[_r(None, None)], ["id", "g"]], "tags": ["edge", "null", "single"]},
    {"id": "h12", "args": [[_r(1, "a"), _r(2, "b")], ["g", "id"]], "tags": ["multi-col"]},
]

_COLS = [["id"], ["g"], ["id", "g"], ["g", "id"]]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 7
        rows = []
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            i = (x >> 8) % 8
            x = (x * 1103515245 + 12345) % 2147483648
            g = "abc"[(x >> 8) % 3]
            x = (x * 1103515245 + 12345) % 2147483648
            if (x >> 8) % 14 == 0:
                i = None
            x = (x * 1103515245 + 12345) % 2147483648
            if (x >> 8) % 14 == 0:
                g = None
            rows.append({"id": i, "g": g})
        x = (x * 1103515245 + 12345) % 2147483648
        cols = list(_COLS[(x >> 8) % len(_COLS)])
        out.append([rows, cols])
    return out


for _i, _a in enumerate(_lcg(23, 14)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
