"""Inputs of check-x422-propagate-routing.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

ALL = [["DEBUG", "a"], ["INFO", "b"], ["WARNING", "c"], ["ERROR", "d"], ["CRITICAL", "e"]]

SAMPLES = [
    {
        "id": "s1",
        "args": ["INFO", "ERROR", [["DEBUG", "a"], ["INFO", "b"], ["ERROR", "c"]], True],
    },
    {"id": "s2", "args": ["DEBUG", "DEBUG", [["INFO", "x"]], False]},
    {"id": "s3", "args": ["WARNING", "DEBUG", [["INFO", "i"], ["WARNING", "w"]], True]},
]

HIDDEN = [
    {"id": "h01", "args": ["DEBUG", "DEBUG", [], True], "tags": ["edge"]},
    {"id": "h02", "args": ["CRITICAL", "DEBUG", ALL, True], "tags": ["edge"]},
    {"id": "h03", "args": ["DEBUG", "DEBUG", ALL, True], "tags": []},
    {"id": "h04", "args": ["DEBUG", "DEBUG", ALL, False], "tags": []},
    {"id": "h05", "args": ["INFO", "WARNING", ALL, True], "tags": []},
    {"id": "h06", "args": ["ERROR", "INFO", ALL, True], "tags": []},
    {"id": "h07", "args": ["WARNING", "CRITICAL", ALL, True], "tags": []},
    {"id": "h08", "args": ["INFO", "ERROR", ALL, False], "tags": []},
    {
        "id": "h09",
        "args": ["ERROR", "ERROR", [["WARNING", "w"], ["ERROR", "x y"]], True],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
