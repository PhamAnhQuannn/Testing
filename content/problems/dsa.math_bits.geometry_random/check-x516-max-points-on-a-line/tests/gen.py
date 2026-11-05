"""Inputs of check-x516-max-points-on-a-line; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 1], [2, 2], [3, 3]]]},
    {"id": "s2", "args": [[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]]},
    {"id": "s3", "args": [[[0, 0], [0, 0], [1, 1]]]},
]


def _points(seed, n, span):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        px = (x >> 8) % (2 * span + 1) - span
        x = (x * 1103515245 + 12345) % 2147483648
        py = (x >> 8) % (2 * span + 1) - span
        out.append([px, py])
    return out


HIDDEN = [
    {"id": "h01", "args": [[[3, 4]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[0, 0], [5, 7]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[2, 2], [2, 2], [2, 2], [2, 2]]], "tags": ["edge"]},
    {"id": "h05", "args": [[[1, 0], [1, 3], [1, -5], [2, 2], [0, 0]]], "tags": []},
    {"id": "h06", "args": [[[0, 1], [4, 1], [-3, 1], [0, 0], [9, 9]]], "tags": []},
    {"id": "h07", "args": [[[0, 0], [1, 1], [1, -1], [2, 2], [2, -2], [3, 3]]], "tags": []},
    {"id": "h08", "args": [[[0, 0], [0, 0], [1, 2], [2, 4], [3, 6], [5, 1]]], "tags": []},
    {"id": "h09", "args": [_points(1, 12, 3)], "tags": []},
    {"id": "h10", "args": [_points(2, 30, 5)], "tags": []},
    {"id": "h11", "args": [_points(3, 60, 8)], "tags": []},
    {"id": "h12", "args": [_points(4, 150, 1000)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
