"""Inputs of check-x426-count-windows; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[2, 1, 5, 1, 3, 2], 3, 3]},
    {"id": "s2", "args": [[4], 1, 4]},
    {"id": "s3", "args": [[1, 1, 1, 1], 2, 2]},
]

HIDDEN = [
    {"id": "h01", "args": [[1, 2, 3, 4, 5], 2, 3], "tags": []},
    {"id": "h02", "args": [[5, 5, 5, 5], 4, 5], "tags": ["edge"]},
    {"id": "h03", "args": [[-1, -2, -3, -4], 2, -3], "tags": []},
    {"id": "h04", "args": [[9], 1, 10], "tags": ["edge"]},
    {"id": "h05", "args": [[3, 1, 4, 1, 5, 9, 2, 6], 3, 4], "tags": []},
    {"id": "h06", "args": [[0, 0, 0, 0, 0], 2, 0], "tags": []},
    {"id": "h07", "args": [[10, -10, 10, -10, 10], 2, 0], "tags": []},
    {"id": "h08", "args": [[1, 2, 3, 4, 5, 6], 6, 3], "tags": ["edge"]},
    {"id": "h09", "args": [[(i * 37) % 11 for i in range(300)], 7, 5], "tags": ["large"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
