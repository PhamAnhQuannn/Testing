"""Inputs of check-x799-fd-violations; `expected` comes from solution.py via gen_hidden."""


def _r(det, dep, pairs):
    return [{det: a, dep: b} for a, b in pairs]


SAMPLES = [
    {
        "id": "s1",
        "args": [_r("zip", "city", [("1", "A"), ("1", "B"), ("2", "C")]), "zip", "city"],
    },
    {
        "id": "s2",
        "args": [_r("zip", "city", [("1", "A"), ("2", "B"), ("1", "A")]), "zip", "city"],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[], "zip", "city"], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [_r("a", "b", [("x", "1")]), "a", "b"], "tags": ["edge", "single"]},
    {
        "id": "h03",
        "args": [_r("a", "b", [("x", "1"), ("y", "2"), ("z", "1")]), "a", "b"],
        "tags": ["holds"],
    },
    {
        "id": "h04",
        "args": [_r("a", "b", [("x", "1"), ("x", "1"), ("x", "1")]), "a", "b"],
        "tags": ["edge", "duplicates"],
    },
    {
        "id": "h05",
        "args": [_r("a", "b", [("x", "1"), ("y", "2"), ("x", "3")]), "a", "b"],
        "tags": ["one-violation"],
    },
    {
        "id": "h06",
        "args": [
            _r("a", "b", [("y", "1"), ("x", "1"), ("y", "2"), ("x", "2"), ("z", "9")]),
            "a",
            "b",
        ],
        "tags": ["multiple-violations", "sorted"],
    },
    {
        "id": "h07",
        "args": [_r("a", "b", [("k", "1"), ("k", "2"), ("k", "3")]), "a", "b"],
        "tags": ["all-same-det"],
    },
    {
        "id": "h08",
        "args": [_r("a", "b", [("k", "1"), ("k", "1")]), "a", "b"],
        "tags": ["all-same-det", "holds"],
    },
    {
        "id": "h09",
        "args": [_r("id", "val", [(3, "p"), (1, "q"), (3, "r"), (2, "q"), (1, "s")]), "id", "val"],
        "tags": ["numeric-det", "multiple-violations"],
    },
    {
        "id": "h10",
        "args": [_r("id", "val", [(10, 1), (9, 2), (10, 1)]), "id", "val"],
        "tags": ["numeric-det", "holds"],
    },
    {
        "id": "h11",
        "args": [
            [{"zip": "7", "city": "A", "name": "n1"}, {"zip": "7", "city": "B", "name": "n1"}],
            "name",
            "city",
        ],
        "tags": ["extra-columns", "swapped-roles"],
    },
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 9
        as_int = (x >> 12) % 2 == 0
        rows = []
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            d = (x >> 8) % 4
            x = (x * 1103515245 + 12345) % 2147483648
            v = (x >> 8) % 3
            if as_int:
                rows.append({"k": d, "v": v})
            else:
                rows.append({"k": "d" + str(d), "v": "v" + str(v)})
        out.append([rows, "k", "v"])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{12 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
