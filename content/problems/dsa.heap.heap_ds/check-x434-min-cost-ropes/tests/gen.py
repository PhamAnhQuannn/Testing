"""Inputs of check-x434. `expected` is recorded from solution.py by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[4, 3, 2, 6]]},
    {"id": "s2", "args": [[1, 2, 3]]},
    {"id": "s3", "args": [[5]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[7]], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 1]], "tags": []},
    {"id": "h04", "args": [[8, 4, 6, 12]], "tags": []},
    {"id": "h05", "args": [[1, 1, 1, 1, 1, 1, 1, 1]], "tags": []},
    {"id": "h06", "args": [[10, 20, 30, 40, 50]], "tags": []},
    {"id": "h07", "args": [[100, 1, 1, 1]], "tags": []},
    {"id": "h08", "args": [[2, 2, 3, 3, 5, 5, 9]], "tags": []},
    {"id": "h09", "args": [[i % 13 + 1 for i in range(2000)]], "tags": ["large"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
