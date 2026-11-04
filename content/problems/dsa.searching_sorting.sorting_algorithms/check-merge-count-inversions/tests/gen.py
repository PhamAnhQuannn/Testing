"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[2, 4, 1, 3, 5]]},
    {"id": "s2", "args": [[5, 4, 3, 2, 1]]},
    {"id": "s3", "args": [[1, 2, 3]]},
]
HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[7]], "tags": []},
    {"id": "h03", "args": [[2, 1]], "tags": []},
    {"id": "h04", "args": [[1, 1, 1]], "tags": []},
    {"id": "h05", "args": [[3, 1, 2, 1]], "tags": []},
    {"id": "h06", "args": [[4, 3, 2, 1, 0, -1]], "tags": []},
    {"id": "h07", "args": [[1, 3, 2, 3, 1]], "tags": []},
    {"id": "h08", "args": [[10, -5, 3, -5, 8, 0]], "tags": []},
    {"id": "h09", "args": [[2, 2, 1, 1]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
