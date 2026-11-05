"""Inputs of check-x476-partition-equal-subset-sum; `expected` comes from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[1, 5, 11, 5]]},
    {"id": "s2", "args": [[1, 2, 3, 5]]},
    {"id": "s3", "args": [[4, 4]]},
]


def _nums(seed, n, hi):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % hi + 1)
    return out


def _even(seed, n, hi):
    v = _nums(seed, n, hi)
    if sum(v) % 2:
        v[0] += 1
    return v


HIDDEN = [
    {"id": "h01", "args": [[7]], "tags": ["edge"]},
    {"id": "h02", "args": [[2, 2]], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 4]], "tags": ["edge"]},
    {"id": "h04", "args": [[100, 1, 1, 1]], "tags": ["edge"]},
    {"id": "h05", "args": [[3, 3, 3, 4, 5]], "tags": []},
    {"id": "h06", "args": [[1] * 40], "tags": []},
    {"id": "h07", "args": [[1, 1, 1, 1, 1, 1, 1, 9]], "tags": []},
    {"id": "h08", "args": [_even(1, 30, 100)], "tags": []},
    {"id": "h09", "args": [_even(2, 50, 100)], "tags": []},
    {"id": "h10", "args": [_nums(3, 45, 100)], "tags": []},
    {"id": "h11", "args": [[97, 89, 83, 79, 73, 71, 67, 61, 59, 53]], "tags": []},
    {"id": "h12", "args": [[100] * 25 + [99, 1]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
