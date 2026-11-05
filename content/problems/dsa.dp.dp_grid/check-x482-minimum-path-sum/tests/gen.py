"""Inputs of check-x482-minimum-path-sum; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 3, 1], [1, 5, 1], [4, 2, 1]]]},
    {"id": "s2", "args": [[[1, 2, 3], [4, 5, 6]]]},
    {"id": "s3", "args": [[[5]]]},
]


def _grid(seed, rows, cols, hi):
    """Seeded LCG grid with values 0..hi."""
    g = []
    x = seed
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append((x >> 8) % (hi + 1))
        g.append(row)
    return g


HIDDEN = [
    {"id": "h01", "args": [[[0]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[3, 1, 4, 1, 5]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[3], [1], [4], [1], [5]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[1, 100], [1, 1]]], "tags": []},
    {"id": "h05", "args": [[[9, 9, 9], [9, 0, 9], [9, 9, 9]]], "tags": []},
    {"id": "h06", "args": [_grid(11, 5, 5, 9)], "tags": []},
    {"id": "h07", "args": [_grid(12, 8, 3, 20)], "tags": []},
    {"id": "h08", "args": [_grid(13, 3, 12, 50)], "tags": []},
    {"id": "h09", "args": [_grid(14, 20, 20, 100)], "tags": []},
    {"id": "h10", "args": [_grid(15, 30, 30, 200)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
