"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 1, 2, 1, 2, 3]]},
    {"id": "s2", "args": [[5, 5, 5, 5]]},
    {"id": "s3", "args": [[1, 2, 3]]},
]
HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[7]], "tags": []},
    {"id": "h03", "args": [[1, 2]], "tags": []},
    {"id": "h04", "args": [[1, 1, 1]], "tags": []},
    {"id": "h05", "args": [[2, 1, 2, 1, 2, 1]], "tags": []},
    {"id": "h06", "args": [[3, 4, 3, 4, 4, 3, 4]], "tags": []},
    {"id": "h07", "args": [[0, 0, 0, 0, 0, 1]], "tags": []},
    {"id": "h08", "args": [[1, 2, 3, 1, 2, 3, 1, 2]], "tags": []},
    {"id": "h09", "args": [[9, 8, 7, 6]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
