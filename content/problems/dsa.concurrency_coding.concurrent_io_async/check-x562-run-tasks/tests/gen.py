"""Inputs of check-x562-run-tasks; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[0, 5, 1], [0, 3, 2], [2, 1, 3]]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for i in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        start = (x >> 8) % 20
        x = (x * 1103515245 + 12345) % 2147483648
        dur = (x >> 8) % 10 + 1
        out.append([start, dur, i + 1])
    return out


HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[[3, 4, 7]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[0, 5, 3], [1, 4, 1], [2, 3, 2]]], "tags": ["tie"]},
    {"id": "h04", "args": [[[0, 2, 4], [0, 5, 2], [0, 1, 9], [0, 3, 1]]], "tags": ["same-start"]},
    {"id": "h05", "args": [[[5, 1, 2], [0, 6, 1], [3, 3, 3], [6, 0, 4]]], "tags": ["tie"]},
    {"id": "h06", "args": [[[0, 0, 5], [0, 0, 2], [0, 0, 9]]], "tags": ["zero"]},
    {"id": "h07", "args": [_lcg(1, 10)], "tags": []},
    {"id": "h08", "args": [_lcg(2, 50)], "tags": []},
    {"id": "h09", "args": [_lcg(3, 200)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
