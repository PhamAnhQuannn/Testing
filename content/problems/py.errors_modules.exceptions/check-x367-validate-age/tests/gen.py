"""Inputs of check-x367-validate-age; expected comes from solution.py."""

SAMPLE = {"id": "s1", "args": [[25, -3, "abc", 0]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3]], "tags": []},
    {"id": "h03", "args": [[-1, -50]], "tags": []},
    {"id": "h04", "args": [["20", None, 3.5]], "tags": []},
    {"id": "h05", "args": [[0, 150, -0, 7]], "tags": []},
    {"id": "h06", "args": [[30, "x", 41, -7, 18]], "tags": []},
    {"id": "h07", "args": [[2.0, [1], {"a": 1}, 9]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
