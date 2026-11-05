"""Inputs of check-x515-min-time-visiting-points; expected comes from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 1], [3, 4], [-1, 0]]]},
    {"id": "s2", "args": [[[3, 2], [-2, 2]]]},
    {"id": "s3", "args": [[[0, 0], [0, 5], [5, 5], [5, 0]]]},
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
    {"id": "h01", "args": [[[5, 5]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[0, 0], [1, 1]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[2, 2], [2, 2], [2, 2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[0, 0], [10, 0], [20, 0]]], "tags": []},
    {"id": "h05", "args": [[[0, 0], [0, -7], [3, -7]]], "tags": []},
    {"id": "h06", "args": [[[-1000, -1000], [1000, 1000]]], "tags": ["edge"]},
    {"id": "h07", "args": [_points(1, 10, 10)], "tags": []},
    {"id": "h08", "args": [_points(2, 25, 50)], "tags": []},
    {"id": "h09", "args": [_points(3, 60, 1000)], "tags": []},
    {"id": "h10", "args": [_points(4, 100, 1000)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
