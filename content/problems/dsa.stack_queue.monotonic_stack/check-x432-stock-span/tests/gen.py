"""Hand-authored inputs; `expected` is recorded from solution.py by gen_hidden.py."""

SAMPLE = {"id": "s1", "args": [[100, 80, 60, 70, 60, 75, 85]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[5]], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3, 4, 5]], "tags": ["edge"]},
    {"id": "h04", "args": [[5, 4, 3, 2, 1]], "tags": ["edge"]},
    {"id": "h05", "args": [[7, 7, 7, 7]], "tags": ["edge"]},
    {"id": "h06", "args": [[31, 41, 48, 59, 79]], "tags": []},
    {"id": "h07", "args": [[10, 4, 5, 90, 120, 80]], "tags": []},
    {"id": "h08", "args": [[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]], "tags": []},
    {"id": "h09", "args": [[2, 2, 1, 1, 3, 3]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
