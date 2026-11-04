"""Inputs of check-x452-count-provinces; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 1, 0], [1, 1, 0], [0, 0, 1]]]},
    {"id": "s2", "args": [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]},
    {"id": "s3", "args": [[[1, 1, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]]]},
]


def _matrix(seed, n, density):
    """Symmetric 0/1 matrix with unit diagonal; `density` is a percentage of linked pairs."""
    m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    x = seed
    for i in range(n):
        for j in range(i + 1, n):
            x = (x * 1103515245 + 12345) % 2147483648
            if (x >> 8) % 100 < density:
                m[i][j] = m[j][i] = 1
    return m


def _chain(n):
    m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n - 1):
        m[i][i + 1] = m[i + 1][i] = 1
    return m


def _isolated(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


HIDDEN = [
    {"id": "h01", "args": [[[1]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[1, 1], [1, 1]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[1, 0], [0, 1]]], "tags": ["edge"]},
    {"id": "h04", "args": [_chain(10)], "tags": []},
    {"id": "h05", "args": [_chain(1)], "tags": ["edge"]},
    {"id": "h05b", "args": [_isolated(12)], "tags": []},
    {"id": "h06", "args": [[[1] * 6 for _ in range(6)]], "tags": []},
    {"id": "h07", "args": [_matrix(1, 15, 5)], "tags": []},
    {"id": "h08", "args": [_matrix(2, 20, 8)], "tags": []},
    {"id": "h09", "args": [_matrix(3, 30, 3)], "tags": []},
    {"id": "h10", "args": [_matrix(4, 120, 1)], "tags": []},
    {"id": "h11", "args": [_chain(150)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
