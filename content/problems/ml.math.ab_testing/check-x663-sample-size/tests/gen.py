"""Inputs of check-x663-sample-size; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [0.05, 0.005]},
    {"id": "s2", "args": [0.5, 0.01]},
]

_PS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.3, 0.5, 0.75]
_MDES = [0.002, 0.004, 0.005, 0.01, 0.02, 0.025, 0.05]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        p = _PS[(x >> 8) % len(_PS)]
        x = (x * 1103515245 + 12345) % 2147483648
        m = _MDES[(x >> 8) % len(_MDES)]
        out.append([p, m])
    return out


HIDDEN = [
    {"id": "h01", "args": [0.5, 0.01], "tags": ["edge"]},
    {"id": "h02", "args": [0.5, 0.001], "tags": ["edge", "huge_n"]},
    {"id": "h03", "args": [0.5, 0.5], "tags": ["edge", "small_n"]},
    {"id": "h04", "args": [0.01, 0.002], "tags": ["edge"]},
    {"id": "h05", "args": [0.05, 0.005], "tags": []},
    {"id": "h06", "args": [0.02, 0.004], "tags": []},
    {"id": "h07", "args": [0.25, 0.025], "tags": []},
    {"id": "h08", "args": [0.1, 0.01], "tags": []},
    {"id": "h09", "args": [0.3, 0.05], "tags": []},
    {"id": "h10", "args": [0.001, 0.0005], "tags": ["edge"]},
]
for _i, _a in enumerate(_lcg(11, 8)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
