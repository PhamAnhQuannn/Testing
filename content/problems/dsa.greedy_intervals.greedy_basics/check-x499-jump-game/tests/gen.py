"""Inputs of check-x499-jump-game; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[2, 3, 1, 1, 4]]},
    {"id": "s2", "args": [[3, 2, 1, 0, 4]]},
    {"id": "s3", "args": [[0]]},
]


def _arr(seed, n, hi, zero_pct):
    """Seeded LCG array of values in 0..hi, with `zero_pct` percent forced to 0."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        v = (x >> 8) % (hi + 1)
        x = (x * 1103515245 + 12345) % 2147483648
        if (x >> 8) % 100 < zero_pct:
            v = 0
        out.append(v)
    return out


HIDDEN = [
    {"id": "h01", "args": [[0]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 0]], "tags": ["edge"]},
    {"id": "h03", "args": [[0, 1]], "tags": ["edge"]},
    {"id": "h04", "args": [[2, 0, 0]], "tags": ["edge"]},
    {"id": "h05", "args": [[1, 1, 0, 1]], "tags": ["edge"]},
    {"id": "h06", "args": [[5, 0, 0, 0, 0, 0]], "tags": []},
    {"id": "h07", "args": [[1] * 50], "tags": []},
    {"id": "h08", "args": [_arr(1, 20, 3, 30)], "tags": []},
    {"id": "h09", "args": [_arr(2, 40, 4, 40)], "tags": []},
    {"id": "h10", "args": [_arr(3, 100, 3, 50)], "tags": []},
    {"id": "h11", "args": [_arr(4, 300, 5, 20)], "tags": []},
    {"id": "h12", "args": [_arr(5, 1000, 2, 45)], "tags": []},
    {"id": "h13", "args": [[3, 2, 1, 0, 4]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
