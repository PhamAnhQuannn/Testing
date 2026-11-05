"""Inputs of check-x472-house-robber; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[2, 7, 9, 3, 1]]},
    {"id": "s2", "args": [[1, 2, 3, 1]]},
    {"id": "s3", "args": [[5]]},
]


def _lcg_list(seed, n, hi):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % (hi + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[7]], "tags": ["edge"]},
    {"id": "h03", "args": [[3, 9]], "tags": ["edge"]},
    {"id": "h04", "args": [[0, 0, 0]], "tags": ["edge"]},
    {"id": "h05", "args": [[2, 1, 1, 2]], "tags": []},
    {"id": "h06", "args": [[100, 1, 1, 100, 1, 1, 100]], "tags": []},
    {"id": "h07", "args": [[400] * 100], "tags": []},
    {"id": "h08", "args": [_lcg_list(1, 10, 400)], "tags": []},
    {"id": "h09", "args": [_lcg_list(2, 25, 400)], "tags": []},
    {"id": "h10", "args": [_lcg_list(3, 60, 400)], "tags": []},
    {"id": "h11", "args": [_lcg_list(4, 100, 400)], "tags": []},
    {"id": "h12", "args": [list(range(1, 51))], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
