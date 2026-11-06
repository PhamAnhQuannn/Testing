"""Inputs of check-x727-parse-ints; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["3 4 5"]},
    {"id": "s2", "args": ["  10   -2 "]},
]

HIDDEN = [
    {"id": "h01", "args": [""], "tags": ["edge"]},
    {"id": "h02", "args": ["   "], "tags": ["edge"]},
    {"id": "h03", "args": ["42"], "tags": ["edge"]},
    {"id": "h04", "args": ["-7"], "tags": ["edge"]},
    {"id": "h05", "args": ["  1    2     3  "], "tags": ["edge"]},
    {"id": "h06", "args": ["1\t2\t-3"], "tags": ["edge"]},
    {"id": "h07", "args": ["5\n6\n7\n"], "tags": ["edge"]},
    {"id": "h08", "args": ["0 0 0"], "tags": []},
    {"id": "h09", "args": ["-1 -2 -3 -4"], "tags": []},
    {"id": "h10", "args": ["100000 -100000 99999"], "tags": []},
]

_SEPS = [" ", "  ", "\t", " \t ", "\n", "   "]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        count = (x >> 8) % 9
        pieces = []
        x = (x * 1103515245 + 12345) % 2147483648
        if (x >> 8) % 2 == 0:
            pieces.append(_SEPS[(x >> 12) % len(_SEPS)])
        for _j in range(count):
            x = (x * 1103515245 + 12345) % 2147483648
            val = (x >> 8) % 2001 - 1000
            x = (x * 1103515245 + 12345) % 2147483648
            pieces.append(str(val))
            pieces.append(_SEPS[(x >> 8) % len(_SEPS)])
        out.append(["".join(pieces)])
    return out


for _i, _a in enumerate(_lcg(17, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
