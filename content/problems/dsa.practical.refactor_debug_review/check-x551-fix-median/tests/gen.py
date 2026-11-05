"""Inputs of check-x551-fix-median; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[3, 1, 2]]},
    {"id": "s2", "args": [[1, 2, 4, 5]]},
    {"id": "s3", "args": [[1, 2]]},
]


def _rand_list(seed, n, lo, hi):
    """Seeded LCG list of n ints in [lo, hi]."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(lo + (x >> 8) % (hi - lo + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [[7]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3, 4, 5]], "tags": []},
    {"id": "h03", "args": [[5, 3, 1, 4, 2]], "tags": []},
    {"id": "h04", "args": [[2, 4]], "tags": ["edge"]},
    {"id": "h05", "args": [[1, 4]], "tags": ["edge"]},
    {"id": "h06", "args": [[-5, -1, -3, -2]], "tags": ["edge"]},
    {"id": "h07", "args": [[-3, -1, -2]], "tags": ["edge"]},
    {"id": "h08", "args": [[1, 2, 3, 4]], "tags": []},
    {"id": "h09", "args": [[4, 4, 4, 4]], "tags": ["edge"]},
    {"id": "h10", "args": [[10, 1, 9, 2, 8, 3]], "tags": []},
    {"id": "h11", "args": [_rand_list(1, 51, -100, 100)], "tags": []},
    {"id": "h12", "args": [_rand_list(2, 200, -1000, 1000)], "tags": []},
    {"id": "h13", "args": [_rand_list(3, 999, -1000000000, 1000000000)], "tags": []},
    {"id": "h14", "args": [_rand_list(4, 1000, 0, 5)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
