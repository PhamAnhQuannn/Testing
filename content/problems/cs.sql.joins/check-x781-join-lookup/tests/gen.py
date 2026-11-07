"""Inputs of check-x781-join-lookup; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [[[1, 10, 50], [2, 20, 30], [3, 99, 40]], [[10, "an"], [20, "binh"]]],
    },
    {"id": "s2", "args": [[], []]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [[10, "an"]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[1, 10, 5]], []], "tags": ["edge"]},
    {"id": "h03", "args": [[[1, 10, 5], [2, 11, 6]], [[12, "x"]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[1, 10, 5], [2, 10, 7], [3, 10, 9]], [[10, "an"]]], "tags": ["edge"]},
    {"id": "h05", "args": [[[1, 10, 5], [2, 10, 7]], [[10, "an"], [10, "binh"]]], "tags": ["edge"]},
    {"id": "h06", "args": [[[2, 20, 1], [1, 10, 2]], [[10, "an"], [20, "binh"]]], "tags": []},
    {
        "id": "h07",
        "args": [[[1, 1, 0], [2, 2, 0]], [[1, "o'brien"], [2, "a;b"]]],
        "tags": ["edge"],
    },
    {"id": "h08", "args": [[[5, 7, 100], [6, 8, 200]], [[7, "x"], [8, "y"], [9, "z"]]], "tags": []},
    {"id": "h09", "args": [[[1, 3, 4], [2, 4, 5], [3, 5, 6]], [[4, "m"]]], "tags": []},
    {"id": "h10", "args": [[[1, 1, 1], [1, 2, 2]], [[1, "p"], [2, "q"]]], "tags": ["edge"]},
]

_NAMES = ["an", "binh", "cuong", "dung", "em", "phuc", "quynh", "o'neil"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_cust = (x >> 8) % 6
        customers = []
        for _c in range(n_cust):
            x = (x * 1103515245 + 12345) % 2147483648
            cid = (x >> 8) % 6
            x = (x * 1103515245 + 12345) % 2147483648
            name = _NAMES[(x >> 8) % len(_NAMES)]
            customers.append([cid, name])
        x = (x * 1103515245 + 12345) % 2147483648
        n_ord = (x >> 8) % 10
        orders = []
        for _o in range(n_ord):
            x = (x * 1103515245 + 12345) % 2147483648
            oid = (x >> 8) % 20
            x = (x * 1103515245 + 12345) % 2147483648
            cid = (x >> 8) % 9
            x = (x * 1103515245 + 12345) % 2147483648
            amount = (x >> 8) % 100
            orders.append([oid, cid, amount])
        out.append([orders, customers])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
