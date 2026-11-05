"""Inputs of check-x553-fix-chunk-average; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4], 2]},
    {"id": "s2", "args": [[1, 2, 3, 4, 5], 2]},
    {"id": "s3", "args": [[10, 20, 30], 1]},
]


def _lcg_list(seed, n, lo, hi):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(lo + (x >> 8) % (hi - lo + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3], 0], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3], -2], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 4], 10], "tags": ["edge"]},
    {"id": "h05", "args": [[5, 7, 9, 11, 13], 1], "tags": ["edge"]},
    {"id": "h06", "args": [[1, 2, 3, 4, 5, 6, 7], 3], "tags": ["edge"]},
    {"id": "h07", "args": [[1, 2, 2, 3], 2], "tags": []},
    {"id": "h08", "args": [[-1, -2, -4, 5, 6], 3], "tags": []},
    {"id": "h09", "args": [_lcg_list(1, 25, -50, 50), 4], "tags": []},
    {"id": "h10", "args": [_lcg_list(2, 60, 0, 100), 7], "tags": []},
    {"id": "h11", "args": [_lcg_list(3, 100, -1000, 1000), 10], "tags": []},
    {"id": "h12", "args": [[4, 4, 4, 4], 4], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
