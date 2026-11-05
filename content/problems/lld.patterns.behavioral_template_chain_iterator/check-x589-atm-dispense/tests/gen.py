"""Inputs of check-x589-atm-dispense; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [1300]},
    {"id": "s2", "args": [30]},
]

HIDDEN = [
    {"id": "h01", "args": [0], "tags": ["edge"]},
    {"id": "h02", "args": [30], "tags": ["edge"]},
    {"id": "h03", "args": [50], "tags": ["single"]},
    {"id": "h04", "args": [500], "tags": ["single"]},
    {"id": "h05", "args": [1000], "tags": ["multiple"]},
    {"id": "h06", "args": [70], "tags": ["undispensable"]},
    {"id": "h07", "args": [1300], "tags": ["basic"]},
    {"id": "h08", "args": [2350], "tags": ["all-denoms"]},
    {"id": "h09", "args": [49], "tags": ["edge"]},
    {"id": "h10", "args": [1000000], "tags": ["large"]},
    {"id": "h11", "args": [999950], "tags": ["large"]},
    {"id": "h12", "args": [1020], "tags": ["undispensable"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    out = []
    x = seed * 7919 + 17
    for i in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        amount = (x >> 8) % 3000
        out.append({"id": f"r{i}", "args": [amount]})
    return out
