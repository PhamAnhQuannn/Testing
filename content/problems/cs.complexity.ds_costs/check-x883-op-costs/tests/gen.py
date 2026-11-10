"""Inputs of check-x883-op-costs; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["array", "index"], ["dict", "get"], ["heap", "push"]]]},
    {"id": "s2", "args": [[["list", "contains"], ["set", "contains"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[["foo", "bar"]]], "tags": ["unknown"]},
    {"id": "h03", "args": [[["array", "index"]]], "tags": ["single"]},
    {
        "id": "h04",
        "args": [[["array", "index"], ["array", "append"], ["dict", "get"], ["dict", "set"]]],
        "tags": ["o1"],
    },
    {
        "id": "h05",
        "args": [[["array", "search"], ["list", "contains"], ["linked_list", "index"]]],
        "tags": ["on"],
    },
    {
        "id": "h06",
        "args": [[["heap", "push"], ["heap", "pop_min"], ["bst", "search"]]],
        "tags": ["ologn"],
    },
    {"id": "h07", "args": [[["sorted", "binary_search"], ["heap", "peek"]]], "tags": ["mix"]},
    {
        "id": "h08",
        "args": [[["dict", "get"], ["dict", "get"], ["dict", "get"]]],
        "tags": ["repeat"],
    },
    {
        "id": "h09",
        "args": [[["array", "insert_front"], ["linked_list", "prepend"]]],
        "tags": ["array-vs-linked"],
    },
    {
        "id": "h10",
        "args": [[["dict", "contains"], ["set", "get"], ["list", "index"]]],
        "tags": ["unknown", "wrong-op"],
    },
    {
        "id": "h11",
        "args": [[["array", "index"], ["foo", "bar"], ["set", "contains"], ["heap", "pop"]]],
        "tags": ["mix", "unknown"],
    },
    {
        "id": "h12",
        "args": [[["Array", "index"], ["", ""], ["dict", "GET"]]],
        "tags": ["case-sensitive", "unknown"],
    },
]

_KNOWN = [
    ["array", "index"],
    ["array", "search"],
    ["array", "append"],
    ["array", "insert_front"],
    ["dict", "get"],
    ["dict", "set"],
    ["set", "contains"],
    ["list", "contains"],
    ["linked_list", "prepend"],
    ["linked_list", "index"],
    ["heap", "push"],
    ["heap", "pop_min"],
    ["heap", "peek"],
    ["bst", "search"],
    ["sorted", "binary_search"],
]
_UNKNOWN = [["foo", "bar"], ["dict", "contains"], ["set", "get"], ["heap", "pop"]]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        m = (x >> 8) % 12
        ops = []
        for _i in range(m):
            x = _next(x)
            if (x >> 8) % 5 == 0:
                x = _next(x)
                ops.append(list(_UNKNOWN[(x >> 8) % len(_UNKNOWN)]))
            else:
                x = _next(x)
                ops.append(list(_KNOWN[(x >> 8) % len(_KNOWN)]))
        out.append([ops])
    return out


for _i, _a in enumerate(_lcg(883, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
