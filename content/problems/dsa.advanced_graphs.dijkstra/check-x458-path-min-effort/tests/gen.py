"""Inputs of check-x458-path-min-effort; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 2, 2], [3, 8, 2], [5, 3, 5]]]},
    {"id": "s2", "args": [[[1, 2, 3], [3, 8, 4], [5, 3, 5]]]},
    {"id": "s3", "args": [[[7]]]},
]


def _grid(seed, rows, cols, maxh):
    """Seeded LCG grid of heights 1..maxh."""
    x = seed
    g = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append((x >> 8) % maxh + 1)
        g.append(row)
    return g


HIDDEN = [
    {"id": "h01", "args": [[[1]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[1, 10]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[1], [5], [2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[3, 3], [3, 3]]], "tags": []},
    {"id": "h05", "args": [[[1, 100, 1], [1, 100, 1], [1, 1, 1]]], "tags": []},
    {"id": "h06", "args": [_grid(1, 5, 5, 20)], "tags": []},
    {"id": "h07", "args": [_grid(2, 8, 6, 100)], "tags": []},
    {"id": "h08", "args": [_grid(3, 1, 20, 50)], "tags": []},
    {"id": "h09", "args": [_grid(4, 20, 1, 50)], "tags": []},
    {"id": "h10", "args": [_grid(5, 30, 30, 1000)], "tags": []},
    {"id": "h11", "args": [_grid(6, 40, 25, 10)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
