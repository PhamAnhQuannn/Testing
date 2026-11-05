"""Inputs of check-x547-life-after; `expected` comes from solution.py via gen_hidden."""

BLINKER = [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
BLOCK = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
GLIDER = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

SAMPLES = [
    {"id": "s1", "args": [[[0, 1, 0], [0, 1, 0], [0, 1, 0]], 1]},
    {"id": "s2", "args": [[[1, 1], [1, 1]], 3]},
    {"id": "s3", "args": [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], 1]},
]


def _pattern(seed, rows, cols, density):
    """Deterministic pseudo-random board; `density` is a percentage of live cells."""
    x = seed
    out = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append(1 if (x >> 8) % 100 < density else 0)
        out.append(row)
    return out


HIDDEN = [
    {"id": "h01", "args": [BLINKER, 0], "tags": ["edge"]},
    {"id": "h02", "args": [[[1]], 1], "tags": ["edge"]},
    {"id": "h03", "args": [BLINKER, 2], "tags": ["edge"]},
    {"id": "h04", "args": [BLOCK, 5], "tags": ["edge"]},
    {"id": "h05", "args": [[[0, 0, 0], [0, 0, 0]], 4], "tags": ["edge"]},
    {"id": "h06", "args": [BLINKER, 1], "tags": []},
    {"id": "h07", "args": [GLIDER, 4], "tags": []},
    {"id": "h08", "args": [[[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1], "tags": []},
    {"id": "h09", "args": [_pattern(1, 8, 8, 40), 6], "tags": []},
    {"id": "h10", "args": [_pattern(2, 12, 7, 35), 10], "tags": []},
    {"id": "h11", "args": [_pattern(3, 30, 30, 30), 20], "tags": []},
    {"id": "h12", "args": [[[1, 0, 1, 1]], 2], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
