"""Inputs for this check; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[3, 1, 5, 8]]},
    {"id": "s2", "args": [[1, 5]]},
    {"id": "s3", "args": [[7]]},
]


def _rand(seed, n, hi):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % (hi + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [[5]], "tags": ["edge"]},
    {"id": "h02", "args": [[]], "tags": ["edge"]},
    {"id": "h03", "args": [[0]], "tags": ["edge"]},
    {"id": "h04", "args": [[2, 2]], "tags": ["edge"]},
    {"id": "h05", "args": [[1] * 10], "tags": []},
    {"id": "h06", "args": [[9, 76, 64, 21, 97, 60]], "tags": []},
    {"id": "h07", "args": [[0, 0, 5, 0, 3]], "tags": []},
    {"id": "h08", "args": [_rand(1, 8, 20)], "tags": []},
    {"id": "h09", "args": [_rand(2, 15, 100)], "tags": []},
    {"id": "h10", "args": [_rand(3, 30, 100)], "tags": []},
    {"id": "h11", "args": [_rand(4, 50, 100)], "tags": []},
    {"id": "h12", "args": [list(range(1, 41))], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
