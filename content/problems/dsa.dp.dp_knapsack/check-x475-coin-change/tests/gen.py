"""Inputs of check-x475-coin-change; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 5], 11]},
    {"id": "s2", "args": [[2], 3]},
    {"id": "s3", "args": [[1], 0]},
]


def _coins(seed, k, hi):
    out = []
    x = seed
    while len(out) < k:
        x = (x * 1103515245 + 12345) % 2147483648
        c = (x >> 8) % hi + 1
        if c not in out:
            out.append(c)
    return out


HIDDEN = [
    {"id": "h01", "args": [[1], 0], "tags": ["edge"]},
    {"id": "h02", "args": [[5], 3], "tags": ["edge"]},
    {"id": "h03", "args": [[2], 1], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 5], 100], "tags": []},
    {"id": "h05", "args": [[186, 419, 83, 408], 6249], "tags": []},
    {"id": "h06", "args": [[2, 4, 6], 7], "tags": ["edge"]},
    {"id": "h07", "args": [[1, 3, 4], 6], "tags": []},
    {"id": "h08", "args": [[7], 49], "tags": []},
    {"id": "h09", "args": [_coins(1, 5, 50), 997], "tags": []},
    {"id": "h10", "args": [_coins(2, 6, 200), 2999], "tags": []},
    {"id": "h11", "args": [[5, 10, 25], 3333], "tags": []},
    {"id": "h12", "args": [[9, 6, 5, 1], 11], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
