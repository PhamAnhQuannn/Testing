"""Inputs of check-x410-slots-probe.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [["x", "y"], ["x", "z"], False]},
    {"id": "s2", "args": [["x"], ["x", "y"], True]},
    {"id": "s3", "args": [[], ["a"], False]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [], False], "tags": ["edge"]},
    {"id": "h02", "args": [[], [], True], "tags": ["edge"]},
    {"id": "h03", "args": [["a", "b"], ["a", "b"], False], "tags": []},
    {"id": "h04", "args": [["a", "b"], ["c", "a", "d"], False], "tags": []},
    {"id": "h05", "args": [["a"], ["a", "b", "c"], True], "tags": []},
    {"id": "h06", "args": [[], ["q", "r"], False], "tags": []},
    {"id": "h07", "args": [[], ["q", "r"], True], "tags": []},
    {"id": "h08", "args": [["x", "y", "z"], ["z", "z", "w"], False], "tags": []},
    {"id": "h09", "args": [["name"], ["name", "age"], False], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
