"""Inputs of check-x409-dynamic-bag.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [{"a": 1, "b": 2}, ["a", "zz"]]},
    {"id": "s2", "args": [{}, ["x"]]},
    {"id": "s3", "args": [{"k": "v"}, ["k", "k"]]},
]

HIDDEN = [
    {"id": "h01", "args": [{}, []], "tags": ["edge"]},
    {"id": "h02", "args": [{}, ["abc"]], "tags": ["edge"]},
    {"id": "h03", "args": [{"a": 1}, ["a"]], "tags": []},
    {"id": "h04", "args": [{"b": 2, "a": 1}, ["a", "b", "c"]], "tags": []},
    {"id": "h05", "args": [{"name": "x", "age": 3}, ["name", "age", "city"]], "tags": []},
    {"id": "h06", "args": [{"z": None}, ["z", "y"]], "tags": []},
    {"id": "h07", "args": [{"q": [1, 2]}, ["q", "w", "e"]], "tags": []},
    {"id": "h08", "args": [{"x": 0, "y": 0, "z": 0}, ["m", "n", "x"]], "tags": []},
    {"id": "h09", "args": [{"a": 1}, ["b", "b"]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
