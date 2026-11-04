"""Inputs of check-x442-ship-capacity; `expected` comes from solution.py via gen_hidden."""

SAMPLE = {"id": "s1", "args": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5]}

SAMPLES = [
    SAMPLE,
    {"id": "s2", "args": [[3, 2, 2, 4, 1, 4], 3]},
    {"id": "s3", "args": [[1, 2, 3, 1, 1], 4]},
]

HIDDEN = [
    {"id": "h01", "args": [[7], 1], "tags": ["edge"]},
    {"id": "h02", "args": [[5, 9, 2, 6], 4], "tags": ["edge"]},
    {"id": "h03", "args": [[5, 9, 2, 6], 1], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 1, 1, 1, 1, 1], 3], "tags": []},
    {"id": "h05", "args": [[10, 50, 10, 50, 10], 2], "tags": []},
    {"id": "h06", "args": [[500, 1, 1, 1, 500], 3], "tags": []},
    {"id": "h07", "args": [[4, 8, 1, 7, 3, 9, 2, 6], 4], "tags": []},
    {"id": "h08", "args": [[250] * 40, 7], "tags": []},
    {"id": "h09", "args": [[1, 500, 1, 500, 1, 500], 2], "tags": []},
    {"id": "h10", "args": [[3, 3, 3, 3], 2], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
