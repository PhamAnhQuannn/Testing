"""Inputs of check-x485-stock-with-cooldown; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 0, 2]]},
    {"id": "s2", "args": [[1]]},
    {"id": "s3", "args": [[6, 1, 3, 2, 4, 7]]},
]


def _prices(seed, n, hi):
    """Seeded LCG price array with values in 0..hi."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % (hi + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[5]], "tags": ["edge"]},
    {"id": "h03", "args": [[9, 8, 7, 6, 5, 4]], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 2, 3, 4, 5]], "tags": []},
    {"id": "h05", "args": [[2, 1]], "tags": ["edge"]},
    {"id": "h06", "args": [[1, 4, 2]], "tags": []},
    {"id": "h07", "args": [[3, 3, 3, 3]], "tags": []},
    {"id": "h08", "args": [_prices(1, 20, 30)], "tags": []},
    {"id": "h09", "args": [_prices(2, 40, 100)], "tags": []},
    {"id": "h10", "args": [_prices(3, 200, 1000)], "tags": []},
    {"id": "h11", "args": [_prices(4, 1000, 1000)], "tags": []},
    {"id": "h12", "args": [_prices(5, 5000, 1000)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
