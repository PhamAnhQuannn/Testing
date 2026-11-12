"""Inputs of check-x886-eval-logic; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["and", True, ["not", False]]]},
    {"id": "s2", "args": [["or", False, False]]},
]

HIDDEN = [
    {"id": "h01", "args": [True], "tags": ["literal-true", "edge"]},
    {"id": "h02", "args": [False], "tags": ["literal-false", "edge"]},
    {"id": "h03", "args": [["not", True]], "tags": ["not"]},
    {"id": "h04", "args": [["not", False]], "tags": ["not"]},
    {"id": "h05", "args": [["and"]], "tags": ["empty-and", "edge"]},
    {"id": "h06", "args": [["or"]], "tags": ["empty-or"]},
    {"id": "h07", "args": [["and", True, True, True, False]], "tags": ["and-many"]},
    {"id": "h08", "args": [["or", False, False, False, True]], "tags": ["or-many"]},
    {"id": "h09", "args": [["not", ["or", True, False]]], "tags": ["nested"]},
    {
        "id": "h10",
        "args": [["or", ["and", True, False], ["and", ["not", False], ["not", False]]]],
        "tags": ["nested"],
    },
    {
        "id": "h11",
        "args": [["not", ["not", ["not", ["not", ["and", True, ["or", False, True]]]]]]],
        "tags": ["deep"],
    },
    {
        "id": "h12",
        "args": [["and", ["or"], ["not", ["and"]], True]],
        "tags": ["mixed", "empty"],
    },
    {
        "id": "h13",
        "args": [["or", ["and"], ["or"]]],
        "tags": ["mixed", "empty"],
    },
    {
        "id": "h14",
        "args": [["and", ["and", ["and", True]], ["or", ["or", False]]]],
        "tags": ["deep"],
    },
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _expr(x, depth):
    x = _next(x)
    r = (x >> 8) % 6
    if depth == 0 or r < 2:
        return x, (x >> 12) % 2 == 0
    if r == 2:
        x, sub = _expr(x, depth - 1)
        return x, ["not", sub]
    op = "and" if r in (3, 4) else "or"
    x = _next(x)
    k = (x >> 8) % 4
    items = [op]
    for _ in range(k):
        x, sub = _expr(x, depth - 1)
        items.append(sub)
    return x, items


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x, e = _expr(x, 4)
        out.append([e])
    return out


for _i, _a in enumerate(_lcg(886, 10)):
    HIDDEN.append({"id": f"h{15 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
