"""Inputs of check-x461; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4]},
    {
        "id": "s2",
        "args": [5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2],
    },
    {"id": "s3", "args": [3, [[0, 1, 1], [1, 2, 1]], 1]},
]


def _graph(seed, n, m, maxw):
    """Seeded LCG random undirected weighted graph without self loops."""
    x = seed
    edges = []
    for _ in range(m):
        x = (x * 1103515245 + 12345) % 2147483648
        u = (x >> 8) % n
        x = (x * 1103515245 + 12345) % 2147483648
        v = (x >> 8) % n
        x = (x * 1103515245 + 12345) % 2147483648
        w = (x >> 8) % maxw + 1
        if u != v:
            edges.append([u, v, w])
    return edges


HIDDEN = [
    {"id": "h01", "args": [1, [], 5], "tags": ["edge"]},
    {"id": "h02", "args": [4, [], 10], "tags": ["edge"]},
    {"id": "h03", "args": [2, [[0, 1, 3]], 2], "tags": ["edge"]},
    {"id": "h04", "args": [2, [[0, 1, 3]], 3], "tags": ["edge"]},
    {"id": "h05", "args": [5, [[0, 1, 1], [2, 3, 1]], 1], "tags": ["edge"]},
    {"id": "h06", "args": [4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]], 1], "tags": []},
    {"id": "h07", "args": [6, [[i, i + 1, 2] for i in range(5)], 4], "tags": []},
    {"id": "h08", "args": [6, [[0, 1, 5], [0, 1, 2], [1, 2, 2]], 3], "tags": []},
    {"id": "h09", "args": [10, _graph(1, 10, 20, 10), 12], "tags": []},
    {"id": "h10", "args": [15, _graph(2, 15, 30, 20), 20], "tags": []},
    {"id": "h11", "args": [20, _graph(3, 20, 40, 50), 40], "tags": []},
    {"id": "h12", "args": [40, _graph(4, 40, 100, 100), 150], "tags": []},
    {"id": "h13", "args": [100, _graph(5, 100, 250, 1000), 1500], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
