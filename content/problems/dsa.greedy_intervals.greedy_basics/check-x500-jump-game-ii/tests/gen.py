"""Inputs of check-x500-jump-game-ii; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[2, 3, 1, 1, 4]]},
    {"id": "s2", "args": [[2, 3, 0, 1, 4]]},
    {"id": "s3", "args": [[0]]},
]


def _arr(seed, n, hi):
    """Seeded LCG array of values in 1..hi (always reachable)."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % hi + 1)
    return out


HIDDEN = [
    {"id": "h01", "args": [[0]], "tags": ["edge"]},
    {"id": "h02", "args": [[1]], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 1]], "tags": ["edge"]},
    {"id": "h04", "args": [[5, 0, 0, 0, 0, 0]], "tags": ["edge"]},
    {"id": "h05", "args": [[1, 2, 0, 1]], "tags": ["edge"]},
    {"id": "h06", "args": [[1] * 50], "tags": []},
    {"id": "h07", "args": [[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1]], "tags": []},
    {"id": "h08", "args": [_arr(1, 20, 3)], "tags": []},
    {"id": "h09", "args": [_arr(2, 60, 4)], "tags": []},
    {"id": "h10", "args": [_arr(3, 200, 5)], "tags": []},
    {"id": "h11", "args": [_arr(4, 500, 8)], "tags": []},
    {"id": "h12", "args": [_arr(5, 1000, 3)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
