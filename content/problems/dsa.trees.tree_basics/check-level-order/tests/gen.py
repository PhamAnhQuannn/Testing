"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[3, 9, 20, None, None, 15, 7]]},
    {"id": "s2", "args": [[1]]},
    {"id": "s3", "args": [[1, 2, 3, 4, 5, 6, 7]]},
]
HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[None]], "tags": []},
    {"id": "h03", "args": [[1, 2]], "tags": []},
    {"id": "h04", "args": [[1, None, 2]], "tags": []},
    {"id": "h05", "args": [[1, None, 2, None, 3]], "tags": []},
    {"id": "h06", "args": [[1, 2, None, 3]], "tags": []},
    {"id": "h07", "args": [[1, 2, 3, None, 4, 5]], "tags": []},
    {"id": "h08", "args": [[5, 4, 8, 11, None, 13, 4, 7, 2]], "tags": []},
    {"id": "h09", "args": [[-1, 0, 1]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
