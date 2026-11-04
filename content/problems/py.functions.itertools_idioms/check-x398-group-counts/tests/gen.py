"""Inputs of check-x398-group-counts.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": [["aa", "b", "cc", "d", "eee"]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [["xyz", "a", "bcd"]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [["solo"]], "tags": ["edge"]},
    {"id": "h03", "args": [["a", "bb", "a", "bb", "a"]], "tags": []},
    {"id": "h04", "args": [["abc", "de", "f", "ghi", "jk", "l"]], "tags": []},
    {"id": "h05", "args": [["", "x", "", "yy"]], "tags": []},
    {"id": "h06", "args": [["same", "four", "word", "test"]], "tags": []},
    {"id": "h07", "args": [["zzzzz", "a", "bb", "ccc", "dddd", "eeeee", "f"]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
