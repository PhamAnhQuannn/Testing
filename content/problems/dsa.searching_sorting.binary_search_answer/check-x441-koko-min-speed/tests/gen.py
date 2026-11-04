"""Inputs of check-x441-koko-min-speed; `expected` comes from solution.py via gen_hidden."""

SAMPLE = {"id": "s1", "args": [[3, 6, 7, 11], 8]}

SAMPLES = [
    SAMPLE,
    {"id": "s2", "args": [[30, 11, 23, 4, 20], 5]},
    {"id": "s3", "args": [[30, 11, 23, 4, 20], 6]},
]

HIDDEN = [
    {"id": "h01", "args": [[10], 3], "tags": ["edge"]},
    {"id": "h02", "args": [[1], 1], "tags": ["edge"]},
    {"id": "h03", "args": [[5, 5, 5, 5], 4], "tags": ["edge"]},
    {"id": "h04", "args": [[1, 1, 1, 1], 10], "tags": []},
    {"id": "h05", "args": [[312884470], 312884469], "tags": []},
    {"id": "h06", "args": [[1000000000, 1000000000], 3], "tags": []},
    {"id": "h07", "args": [[9, 3, 7, 12, 15, 2], 10], "tags": []},
    {"id": "h08", "args": [[100, 1, 1, 1], 6], "tags": []},
    {"id": "h09", "args": [[805306368, 805306368, 805306368], 1000000000], "tags": []},
    {"id": "h10", "args": [[2, 2], 2], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
