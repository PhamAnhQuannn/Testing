"""Inputs of check-x454-count-reachable; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [4, [[0, 1], [1, 2], [3, 0]], 0]},
    {"id": "s2", "args": [3, [], 1]},
    {"id": "s3", "args": [5, [[0, 1], [1, 0], [1, 2], [2, 2], [3, 4]], 0]},
]


def _random_edges(seed, n, m):
    """`m` pseudo-random directed edges from a seeded LCG."""
    x = seed
    edges = []
    for _ in range(m):
        x = (x * 1103515245 + 12345) % 2147483648
        u = (x >> 8) % n
        x = (x * 1103515245 + 12345) % 2147483648
        v = (x >> 8) % n
        edges.append([u, v])
    return edges


def _path(n):
    return [[i, i + 1] for i in range(n - 1)]


HIDDEN = [
    {"id": "h01", "args": [1, [], 0], "tags": ["edge"]},
    {"id": "h02", "args": [1, [[0, 0]], 0], "tags": ["edge"]},
    {"id": "h03", "args": [2, [[0, 1]], 1], "tags": ["edge"]},
    {"id": "h04", "args": [2, [[0, 1]], 0], "tags": []},
    {"id": "h05", "args": [10, _path(10), 0], "tags": []},
    {"id": "h06", "args": [10, _path(10), 9], "tags": []},
    {"id": "h07", "args": [6, [[0, 1], [1, 2], [2, 0], [3, 4]], 2], "tags": []},
    {"id": "h08", "args": [15, _random_edges(1, 15, 14), 0], "tags": []},
    {"id": "h09", "args": [30, _random_edges(2, 30, 35), 3], "tags": []},
    {"id": "h10", "args": [50, _random_edges(3, 50, 40), 7], "tags": []},
    {"id": "h11", "args": [500, _path(500), 0], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
