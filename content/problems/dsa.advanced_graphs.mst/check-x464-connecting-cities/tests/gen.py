"""Inputs of check-x464-connecting-cities; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]]},
    {"id": "s2", "args": [4, [[1, 2, 3], [3, 4, 4]]]},
    {"id": "s3", "args": [4, [[1, 2, 1], [2, 3, 2], [3, 4, 3], [1, 4, 10], [1, 3, 5]]]},
]


def _edges(seed, n, m, max_cost):
    x = seed
    out = []
    for _ in range(m):
        x = (x * 1103515245 + 12345) % 2147483648
        u = (x >> 8) % n + 1
        x = (x * 1103515245 + 12345) % 2147483648
        v = (x >> 8) % n + 1
        x = (x * 1103515245 + 12345) % 2147483648
        c = (x >> 8) % max_cost + 1
        if u != v:
            out.append([u, v, c])
    return out


def _path(n, c):
    return [[i, i + 1, c + i] for i in range(1, n)]


HIDDEN = [
    {"id": "h01", "args": [1, []], "tags": ["edge"]},
    {"id": "h02", "args": [2, []], "tags": ["edge"]},
    {"id": "h03", "args": [2, [[1, 2, 7]]], "tags": ["edge"]},
    {"id": "h04", "args": [4, [[1, 2, 1], [3, 4, 1]]], "tags": ["edge"]},
    {"id": "h05", "args": [5, [[1, 2, 3], [1, 2, 1], [2, 1, 2], [2, 3, 4]]], "tags": []},
    {"id": "h06", "args": [20, _path(20, 5)], "tags": []},
    {"id": "h07", "args": [10, _edges(1, 10, 25, 20)], "tags": []},
    {"id": "h08", "args": [30, _edges(2, 30, 90, 100)], "tags": []},
    {"id": "h09", "args": [50, _edges(3, 50, 40, 1000)], "tags": []},
    {"id": "h10", "args": [100, _edges(4, 100, 600, 10000)], "tags": []},
    {"id": "h11", "args": [200, _edges(5, 200, 1500, 100000)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
