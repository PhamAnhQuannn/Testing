"""Inputs of check-x766-orm-filter; `expected` comes from solution.py via gen_hidden."""


def _r(name, age):
    return {"name": name, "age": age}


_ROWS = [_r("a", 30), _r("b", 25), _r("c", 30)]
_TIES = [_r("bo", 20), _r("an", 20), _r("cy", 10), _r("an", 10), _r("bo", 10)]

SAMPLES = [
    {"id": "s1", "args": [_ROWS, {"age": 30}, ["name"]]},
    {"id": "s2", "args": [[], {"age": 30}, ["name"]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], {}, []], "tags": ["edge"]},
    {"id": "h02", "args": [_ROWS, {}, []], "tags": ["edge"]},
    {"id": "h03", "args": [_ROWS, {"age": 99}, ["name"]], "tags": ["edge"]},
    {"id": "h04", "args": [_ROWS, {"age": 30}, []], "tags": ["edge"]},
    {"id": "h05", "args": [_TIES, {}, ["age"]], "tags": ["edge"]},
    {"id": "h06", "args": [_TIES, {}, ["age", "name"]], "tags": ["edge"]},
    {"id": "h07", "args": [_TIES, {}, ["name", "age"]], "tags": []},
    {"id": "h08", "args": [_TIES, {"name": "an"}, ["age"]], "tags": []},
    {"id": "h09", "args": [_TIES, {"name": "bo", "age": 10}, ["name"]], "tags": ["edge"]},
    {"id": "h10", "args": [_ROWS, {"name": "a", "age": 25}, ["age"]], "tags": ["edge"]},
    {"id": "h11", "args": [[_r("z", 1), _r("z", 1)], {"name": "z"}, ["age", "name"]], "tags": []},
    {"id": "h12", "args": [_ROWS, {}, ["age", "name"]], "tags": []},
]

_NAMES = ["an", "binh", "chi", "dung", "em"]
_AGES = [10, 20, 30]
_ORDERS = [[], ["name"], ["age"], ["age", "name"], ["name", "age"]]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rows = (x >> 8) % 9
        rows = []
        for _r_i in range(n_rows):
            x = (x * 1103515245 + 12345) % 2147483648
            name = _NAMES[(x >> 8) % len(_NAMES)]
            x = (x * 1103515245 + 12345) % 2147483648
            age = _AGES[(x >> 8) % len(_AGES)]
            rows.append({"name": name, "age": age})
        x = (x * 1103515245 + 12345) % 2147483648
        mode = (x >> 8) % 4
        conds = {}
        if mode in (1, 3):
            x = (x * 1103515245 + 12345) % 2147483648
            conds["name"] = _NAMES[(x >> 8) % len(_NAMES)]
        if mode in (2, 3):
            x = (x * 1103515245 + 12345) % 2147483648
            conds["age"] = _AGES[(x >> 8) % len(_AGES)]
        x = (x * 1103515245 + 12345) % 2147483648
        order_by = list(_ORDERS[(x >> 8) % len(_ORDERS)])
        out.append([rows, conds, order_by])
    return out


for _i, _a in enumerate(_lcg(29, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
