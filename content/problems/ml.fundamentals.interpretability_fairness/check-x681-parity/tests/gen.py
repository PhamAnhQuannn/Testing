"""Inputs of check-x681-parity; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [60, 100, 30, 100]},
    {"id": "s2", "args": [1, 3, 2, 7]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        at = (x >> 8) % 41
        x = (x * 1103515245 + 12345) % 2147483648
        aa = (x >> 8) % (at + 1)
        x = (x * 1103515245 + 12345) % 2147483648
        bt = (x >> 8) % 41
        x = (x * 1103515245 + 12345) % 2147483648
        ba = (x >> 8) % (bt + 1)
        out.append([aa, at, ba, bt])
    return out


HIDDEN = [
    {"id": "h01", "args": [50, 100, 25, 50], "tags": ["equal"]},
    {"id": "h02", "args": [0, 0, 5, 10], "tags": ["edge"]},
    {"id": "h03", "args": [0, 0, 0, 0], "tags": ["edge"]},
    {"id": "h04", "args": [10, 10, 0, 10], "tags": ["extreme"]},
    {"id": "h05", "args": [30, 100, 60, 100], "tags": ["reversed"]},
    {"id": "h06", "args": [1, 3, 2, 7], "tags": ["mixed"]},
    {"id": "h07", "args": [7, 9, 0, 0], "tags": ["edge"]},
]
for _i, _a in enumerate(_lcg(11, 8)):
    HIDDEN.append({"id": f"h{8 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
