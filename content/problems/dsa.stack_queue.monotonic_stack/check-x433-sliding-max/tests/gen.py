"""Hand-authored inputs; `expected` is recorded from solution.py by gen_hidden.py."""

SAMPLE = {"id": "s1", "args": [[1, 3, -1, -3, 5, 3, 6, 7], 3]}

HIDDEN = [
    {"id": "h01", "args": [[], 1], "tags": ["edge"]},
    {"id": "h02", "args": [[4], 1], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3, 4, 5], 2], "tags": ["edge"]},
    {"id": "h04", "args": [[5, 4, 3, 2, 1], 3], "tags": ["edge"]},
    {"id": "h05", "args": [[2, 2, 2, 2], 2], "tags": ["edge"]},
    {"id": "h06", "args": [[9, 11], 2], "tags": []},
    {"id": "h07", "args": [[4, -2], 1], "tags": []},
    {"id": "h08", "args": [[7, 2, 4], 2], "tags": []},
    {"id": "h09", "args": [[1, -1], 1], "tags": []},
    {"id": "h10", "args": [[3, 1, 2, 0, 5, 4, 4, 1], 4], "tags": []},
    {"id": "h11", "args": [[1, 3, 1, 2, 0, 5], 3], "tags": []},
    {"id": "h12", "args": [[8, 8, 1, 9, 2, 2, 7], 7], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
