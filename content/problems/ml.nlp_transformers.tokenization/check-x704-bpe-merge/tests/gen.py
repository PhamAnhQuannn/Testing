"""Inputs of check-x704-bpe-merge; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["l", "o", "w", "e", "r"], ["l", "o"]]},
    {"id": "s2", "args": [["a", "a", "a"], ["a", "a"]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], ["a", "b"]], "tags": ["edge"]},
    {"id": "h02", "args": [["a"], ["a", "a"]], "tags": ["edge"]},
    {"id": "h03", "args": [["a", "a", "a", "a"], ["a", "a"]], "tags": ["edge"]},
    {"id": "h04", "args": [["a", "a", "a", "a", "a"], ["a", "a"]], "tags": ["edge"]},
    {"id": "h05", "args": [["x", "y", "z"], ["a", "b"]], "tags": ["edge"]},
    {"id": "h06", "args": [["l", "o", "w", "l", "o", "w", "e", "r"], ["l", "o"]], "tags": []},
    {"id": "h07", "args": [["lo", "w", "lo", "w"], ["lo", "w"]], "tags": []},
    {"id": "h08", "args": [["a", "b", "a", "b", "a"], ["a", "b"]], "tags": []},
    {"id": "h09", "args": [["b", "a", "b", "a"], ["a", "b"]], "tags": ["edge"]},
    {"id": "h10", "args": [["a", "b"], ["a", "b"]], "tags": ["edge"]},
]

_ALPHA = ["a", "b", "c", "ab"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 11
        tokens = []
        for _j in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            tokens.append(_ALPHA[(x >> 8) % len(_ALPHA)])
        x = (x * 1103515245 + 12345) % 2147483648
        first = _ALPHA[(x >> 8) % len(_ALPHA)]
        x = (x * 1103515245 + 12345) % 2147483648
        second = _ALPHA[(x >> 8) % len(_ALPHA)]
        out.append([tokens, [first, second]])
    return out


for _i, _a in enumerate(_lcg(17, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
