"""Inputs of check-x787-rank-within; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["a", "x", 5], ["a", "y", 9], ["b", "z", 1]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["a", "x", 4]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["a", "x", 1], ["a", "y", 2], ["a", "z", 3]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", "mia", 5], ["a", "bob", 5], ["a", "zed", 5]]], "tags": ["edge"]},
    {
        "id": "h05",
        "args": [[["b", "p", 2], ["a", "q", 7], ["b", "r", 9], ["a", "s", 1]]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "args": [[["g'1", "o'brien", 3], ["g'1", "a;b", 3], ['g"2', "x", 1]]],
        "tags": ["edge"],
    },
    {"id": "h07", "args": [[["a", "x", -3], ["a", "y", -7], ["a", "z", 0]]], "tags": ["edge"]},
    {"id": "h08", "args": [[["a", "x", 5], ["a", "x", 5], ["b", "x", 5]]], "tags": ["edge"]},
    {
        "id": "h09",
        "args": [[["c", "n1", 8], ["a", "n2", 8], ["b", "n3", 8], ["a", "n4", 9], ["c", "n5", 2]]],
        "tags": [],
    },
    {"id": "h10", "args": [[["z", "a", 1], ["y", "b", 1], ["x", "c", 1]]], "tags": ["edge"]},
]

_GRPS = ["a", "b", "c", "d"]
_NAMES = ["ann", "bob", "cy", "dee", "eli", "fay", "gus", "hal"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rows = (x >> 8) % 12
        rows = []
        for _r in range(n_rows):
            x = (x * 1103515245 + 12345) % 2147483648
            grp = _GRPS[(x >> 8) % len(_GRPS)]
            x = (x * 1103515245 + 12345) % 2147483648
            name = _NAMES[(x >> 8) % len(_NAMES)]
            x = (x * 1103515245 + 12345) % 2147483648
            score = (x >> 8) % 7 - 3
            rows.append([grp, name, score])
        out.append([rows])
    return out


for _i, _a in enumerate(_lcg(41, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
