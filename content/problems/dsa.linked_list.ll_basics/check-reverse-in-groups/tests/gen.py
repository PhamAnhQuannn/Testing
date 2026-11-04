"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3, 4, 5], 2]},
    {"id": "s2", "args": [[1, 2, 3, 4, 5, 6], 3]},
    {"id": "s3", "args": [[1, 2, 3], 1]},
]
HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge"]},
    {"id": "h02", "args": [[1], 1], "tags": []},
    {"id": "h03", "args": [[1], 2], "tags": []},
    {"id": "h04", "args": [[1, 2, 3, 4], 4], "tags": []},
    {"id": "h05", "args": [[1, 2, 3, 4], 5], "tags": []},
    {"id": "h06", "args": [[1, 2, 3, 4, 5, 6, 7], 3], "tags": []},
    {"id": "h07", "args": [[5, 4, 3, 2, 1, 0], 2], "tags": []},
    {"id": "h08", "args": [[1, 1, 2, 2, 3, 3], 2], "tags": []},
    {"id": "h09", "args": [[9, 8, 7, 6, 5], 5], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
