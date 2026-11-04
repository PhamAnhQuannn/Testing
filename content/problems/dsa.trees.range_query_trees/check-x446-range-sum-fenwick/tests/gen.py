"""Inputs of check-x446-range-sum-fenwick; `expected` comes from solution.py via gen_hidden."""

SAMPLE = {"id": "s1", "args": [[3, 2, -1, 6, 5, 4], [[0, 5], [1, 3], [2, 2], [4, 5]]]}

SAMPLES = [
    SAMPLE,
    {"id": "s2", "args": [[1, 2, 3, 4, 5], [[0, 0], [0, 4], [1, 3]]]},
    {"id": "s3", "args": [[-5, 10, -3, 8], [[0, 3], [1, 2], [3, 3]]]},
]


def _lcg(seed, n, lo, hi):
    out, x = [], seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(lo + x % (hi - lo + 1))
    return out


def _queries(seed, n, q):
    raw = _lcg(seed, 2 * q, 0, n - 1)
    return [[min(raw[2 * i], raw[2 * i + 1]), max(raw[2 * i], raw[2 * i + 1])] for i in range(q)]


_BIG = _lcg(7, 2000, -1000000000, 1000000000)

HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge"]},
    {"id": "h02", "args": [[7], [[0, 0]]], "tags": ["edge"]},
    {"id": "h03", "args": [[5, -5, 5, -5], [[0, 1], [0, 3], [1, 2]]], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 1, 1, 1, 1, 1, 1, 1], [[0, 7], [0, 0], [7, 7], [3, 4]]], "tags": []},
    {"id": "h05", "args": [[1000000000] * 6, [[0, 5], [2, 3]]], "tags": []},
    {"id": "h06", "args": [[-1000000000] * 5, [[0, 4], [1, 1]]], "tags": []},
    {"id": "h07", "args": [[0, 0, 0, 0], [[0, 3], [2, 2]]], "tags": []},
    {
        "id": "h08",
        "args": [list(range(1, 17)), [[0, 15], [4, 11], [7, 8], [0, 7], [8, 15]]],
        "tags": [],
    },
    {"id": "h09", "args": [_BIG, _queries(11, 2000, 500)], "tags": []},
    {"id": "h10", "args": [[4, 2, 7], []], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
