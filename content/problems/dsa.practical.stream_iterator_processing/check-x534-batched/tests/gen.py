"""Inputs of check-x534-batched; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4, 5], 2]},
    {"id": "s2", "args": [[1, 2, 3, 4], 2]},
    {"id": "s3", "args": [[7, 8, 9], 5]},
]


def _lcg_list(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % 2001 - 1000)
    return out


HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3], 0], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3], -2], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 3], 10], "tags": ["edge"]},
    {"id": "h05", "args": [[4, 5, 6, 7], 1], "tags": ["edge"]},
    {"id": "h06", "args": [[9], 1], "tags": ["edge"]},
    {"id": "h07", "args": [[1, 2, 3, 4, 5, 6], 3], "tags": []},
    {"id": "h08", "args": [[1, 2, 3, 4, 5, 6, 7], 3], "tags": []},
    {"id": "h09", "args": [_lcg_list(1, 50), 7], "tags": []},
    {"id": "h10", "args": [_lcg_list(2, 200), 13], "tags": []},
    {"id": "h11", "args": [_lcg_list(3, 1000), 1000], "tags": []},
    {"id": "h12", "args": [_lcg_list(4, 1000), 999], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
