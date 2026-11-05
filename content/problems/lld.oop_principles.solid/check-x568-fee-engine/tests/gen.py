"""Inputs of check-x568-fee-engine; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["bike", 100], ["car", 50]]]},
    {"id": "s2", "args": [[["truck", 10], ["van", 7]]]},
]

KINDS = ["bike", "car", "truck", "van", "boat"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        kind = KINDS[(x >> 8) % len(KINDS)]
        x = (x * 1103515245 + 12345) % 2147483648
        out.append([kind, (x >> 8) % 1000])
    return out


HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[["car", 25]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["plane", 40], ["bike", 3]]], "tags": ["unknown"]},
    {"id": "h04", "args": [[["bike", 10], ["car", 10], ["truck", 10]]], "tags": ["all"]},
    {"id": "h05", "args": [[["truck", 0], ["car", 0]]], "tags": ["zero"]},
    {"id": "h06", "args": [[["truck", 100000]] * 1000], "tags": ["large"]},
    {"id": "h07", "args": [_lcg(1, 10)], "tags": []},
    {"id": "h08", "args": [_lcg(2, 100)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
