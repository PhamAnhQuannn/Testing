"""Inputs of check-x460; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1],
    },
    {"id": "s2", "args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1]},
    {"id": "s3", "args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0]},
]


def _graph(seed, n, m, maxw):
    """Seeded LCG random directed graph without self loops."""
    x = seed
    flights = []
    for _ in range(m):
        x = (x * 1103515245 + 12345) % 2147483648
        u = (x >> 8) % n
        x = (x * 1103515245 + 12345) % 2147483648
        v = (x >> 8) % n
        x = (x * 1103515245 + 12345) % 2147483648
        w = (x >> 8) % maxw + 1
        if u != v:
            flights.append([u, v, w])
    return flights


HIDDEN = [
    {"id": "h01", "args": [2, [[0, 1, 5]], 0, 1, 0], "tags": ["edge"]},
    {"id": "h02", "args": [3, [[0, 1, 5]], 0, 2, 3], "tags": ["edge"]},
    {"id": "h03", "args": [3, [[1, 0, 5]], 0, 1, 2], "tags": ["edge"]},
    {"id": "h04", "args": [3, [[0, 1, 1], [1, 2, 1], [0, 2, 5]], 0, 2, 0], "tags": []},
    {"id": "h05", "args": [3, [[0, 1, 1], [1, 2, 1], [0, 2, 5]], 0, 2, 1], "tags": []},
    {
        "id": "h06",
        "args": [5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [0, 4, 10]], 0, 4, 2],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [0, 4, 10]], 0, 4, 3],
        "tags": [],
    },
    {"id": "h08", "args": [4, [[0, 1, 1], [1, 0, 1], [1, 2, 1], [2, 3, 1]], 0, 3, 5], "tags": []},
    {"id": "h09", "args": [10, _graph(1, 10, 30, 50), 0, 9, 2], "tags": []},
    {"id": "h10", "args": [15, _graph(2, 15, 50, 100), 3, 12, 3], "tags": []},
    {"id": "h11", "args": [20, _graph(3, 20, 80, 100), 0, 19, 1], "tags": []},
    {"id": "h12", "args": [50, _graph(4, 50, 200, 1000), 5, 40, 6], "tags": []},
    {"id": "h13", "args": [100, _graph(5, 100, 400, 10000), 0, 99, 98], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
