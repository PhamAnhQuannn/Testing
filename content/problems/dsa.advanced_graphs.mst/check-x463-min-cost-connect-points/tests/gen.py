"""Inputs of check-x463-min-cost-connect-points; `expected` comes from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]]},
    {"id": "s2", "args": [[[3, 12], [-2, 5], [-4, 1]]]},
    {"id": "s3", "args": [[[0, 0], [1, 1], [1, 0], [-1, 1]]]},
]


def _points(seed, n, span):
    """Points from a seeded LCG, coordinates in [-span, span]."""
    x = seed
    pts = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        px = (x >> 8) % (2 * span + 1) - span
        x = (x * 1103515245 + 12345) % 2147483648
        py = (x >> 8) % (2 * span + 1) - span
        pts.append([px, py])
    return pts


HIDDEN = [
    {"id": "h01", "args": [[[0, 0]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[0, 0], [3, 4]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[1, 1], [1, 1], [1, 1]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[i, 0] for i in range(10)]], "tags": []},
    {"id": "h05", "args": [[[-1000000, -1000000], [1000000, 1000000]]], "tags": ["edge"]},
    {"id": "h06", "args": [_points(1, 8, 10)], "tags": []},
    {"id": "h07", "args": [_points(2, 15, 50)], "tags": []},
    {"id": "h08", "args": [_points(3, 30, 1000)], "tags": []},
    {"id": "h09", "args": [_points(4, 60, 5)], "tags": []},
    {"id": "h10", "args": [_points(5, 100, 1000000)], "tags": []},
    {"id": "h11", "args": [_points(6, 150, 100)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
