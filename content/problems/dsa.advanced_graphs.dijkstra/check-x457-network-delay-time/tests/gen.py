"""Inputs of check-x457-network-delay-time; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2]},
    {"id": "s2", "args": [[[1, 2, 1]], 2, 1]},
    {"id": "s3", "args": [[[1, 2, 1]], 2, 2]},
]


def _graph(seed, n, m, maxw):
    """Seeded LCG random directed graph: m edges over nodes 1..n, weights 1..maxw."""
    x = seed
    edges = []
    for _ in range(m):
        x = (x * 1103515245 + 12345) % 2147483648
        u = (x >> 8) % n + 1
        x = (x * 1103515245 + 12345) % 2147483648
        v = (x >> 8) % n + 1
        x = (x * 1103515245 + 12345) % 2147483648
        w = (x >> 8) % maxw + 1
        edges.append([u, v, w])
    return edges


def _chain(n):
    return [[i, i + 1, 2] for i in range(1, n)]


HIDDEN = [
    {"id": "h01", "args": [[], 1, 1], "tags": ["edge"]},
    {"id": "h02", "args": [[[1, 2, 5]], 3, 1], "tags": ["edge"]},
    {"id": "h03", "args": [[[2, 1, 3]], 2, 1], "tags": ["edge"]},
    {"id": "h04", "args": [[[1, 2, 1], [2, 3, 2], [1, 3, 10]], 3, 1], "tags": []},
    {"id": "h05", "args": [[[1, 2, 1], [1, 2, 4], [2, 1, 1]], 2, 1], "tags": []},
    {"id": "h06", "args": [_chain(50), 50, 1], "tags": []},
    {"id": "h07", "args": [_chain(50), 50, 25], "tags": []},
    {"id": "h08", "args": [_graph(1, 10, 30, 9), 10, 1], "tags": []},
    {"id": "h09", "args": [_graph(2, 20, 80, 20), 20, 3], "tags": []},
    {"id": "h10", "args": [_graph(3, 30, 40, 5), 30, 7], "tags": []},
    {"id": "h11", "args": [_graph(4, 100, 600, 100), 100, 50], "tags": []},
    {"id": "h12", "args": [_graph(5, 100, 150, 100), 100, 1], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
