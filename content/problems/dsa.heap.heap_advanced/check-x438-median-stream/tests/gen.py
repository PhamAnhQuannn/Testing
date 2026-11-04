"""Inputs of check-x438-median-stream. `expected` is recorded from solution.py by gen_hidden."""

SAMPLE = {"id": "s1", "args": [[5, 2, 8, 1]]}
SAMPLES = [
    SAMPLE,
    {"id": "s2", "args": [[3]]},
    {"id": "s3", "args": [[1, 2, 3, 4]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[-1]], "tags": ["edge"]},
    {"id": "h03", "args": [[7, 7, 7, 7]], "tags": []},
    {"id": "h04", "args": [[5, 4, 3, 2, 1]], "tags": []},
    {"id": "h05", "args": [[-5, 10, -3, 8, 0, 0]], "tags": []},
    {"id": "h06", "args": [[1, 100, 1, 100, 1, 100]], "tags": []},
    {"id": "h07", "args": [[2, 1]], "tags": []},
    {"id": "h08", "args": [[(i * 37) % 101 - 50 for i in range(300)]], "tags": []},
    {"id": "h09", "args": [[9, -9, 9, -9, 9]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
