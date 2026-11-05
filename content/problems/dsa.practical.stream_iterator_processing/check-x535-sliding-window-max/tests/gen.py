"""Inputs of check-x535-sliding-window-max; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 3, -1, -3, 5, 3, 6, 7], 3]},
    {"id": "s2", "args": [[4, 2, 12, 3], 1]},
    {"id": "s3", "args": [[5, 1, 2], 5]},
]


def _lcg_list(seed, n, span=20001):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % span - span // 2)
    return out


HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3], 0], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3], -1], "tags": ["edge"]},
    {"id": "h04", "args": [[3, 1, 2], 3], "tags": ["edge"]},
    {"id": "h05", "args": [[3, 1, 2], 10], "tags": ["edge"]},
    {"id": "h06", "args": [[5, 4, 3, 9, 1], 1], "tags": ["edge"]},
    {"id": "h07", "args": [[7], 1], "tags": ["edge"]},
    {"id": "h08", "args": [[2, 2, 2, 2, 2], 2], "tags": []},
    {"id": "h09", "args": [list(range(10)), 4], "tags": []},
    {"id": "h10", "args": [list(range(10, 0, -1)), 4], "tags": []},
    {"id": "h11", "args": [_lcg_list(1, 60), 5], "tags": []},
    {"id": "h12", "args": [_lcg_list(2, 300), 17], "tags": []},
    {"id": "h13", "args": [_lcg_list(3, 2000), 100], "tags": []},
    {"id": "h14", "args": [_lcg_list(4, 2000), 1999], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
