"""Inputs of check-x484-stock-with-fee; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 3, 2, 8, 4, 9], 2]},
    {"id": "s2", "args": [[1, 3, 7, 5, 10, 3], 3]},
    {"id": "s3", "args": [[5, 4, 3, 2], 1]},
]


def _prices(seed, n, hi):
    """Seeded LCG price array with values in 1..hi."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(1 + (x >> 8) % hi)
    return out


HIDDEN = [
    {"id": "h01", "args": [[], 2], "tags": ["edge"]},
    {"id": "h02", "args": [[7], 1], "tags": ["edge"]},
    {"id": "h03", "args": [[9, 8, 7, 6, 5, 4], 0], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 3, 4, 5], 1], "tags": []},
    {"id": "h05", "args": [[1, 5], 10], "tags": ["edge"]},
    {"id": "h06", "args": [[1, 4, 6, 2, 8, 3, 10, 14], 3], "tags": []},
    {"id": "h07", "args": [_prices(1, 20, 30), 2], "tags": []},
    {"id": "h08", "args": [_prices(2, 40, 100), 5], "tags": []},
    {"id": "h09", "args": [_prices(3, 100, 50), 0], "tags": []},
    {"id": "h10", "args": [_prices(4, 500, 1000), 20], "tags": []},
    {"id": "h11", "args": [_prices(5, 3000, 49999), 100], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
