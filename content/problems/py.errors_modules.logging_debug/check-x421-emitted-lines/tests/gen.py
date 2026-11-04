"""Inputs of check-x421-emitted-lines.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {
        "id": "s1",
        "args": ["WARNING", [["DEBUG", "a"], ["INFO", "b"], ["WARNING", "c"], ["ERROR", "d"]]],
    },
    {"id": "s2", "args": ["DEBUG", [["DEBUG", "x"], ["INFO", "y"]]]},
    {"id": "s3", "args": ["CRITICAL", [["ERROR", "e"], ["CRITICAL", "boom"]]]},
]

HIDDEN = [
    {"id": "h01", "args": ["INFO", []], "tags": ["edge"]},
    {"id": "h02", "args": ["ERROR", [["DEBUG", "a"], ["INFO", "b"]]], "tags": ["edge"]},
    {"id": "h03", "args": ["DEBUG", [["CRITICAL", "c"]]], "tags": []},
    {
        "id": "h04",
        "args": ["INFO", [["INFO", "start"], ["DEBUG", "skip"], ["INFO", "end"]]],
        "tags": [],
    },
    {"id": "h05", "args": ["WARNING", [["WARNING", "w1"], ["WARNING", "w2"]]], "tags": []},
    {
        "id": "h06",
        "args": [
            "ERROR",
            [["WARNING", "w"], ["ERROR", "e"], ["CRITICAL", "c"], ["INFO", "i"]],
        ],
        "tags": [],
    },
    {"id": "h07", "args": ["INFO", [["INFO", "a b c"], ["ERROR", "x:y"]]], "tags": []},
    {"id": "h08", "args": ["CRITICAL", [["DEBUG", "d"], ["CRITICAL", ""]]], "tags": []},
    {"id": "h09", "args": ["DEBUG", [["DEBUG", "1"], ["INFO", "2"], ["WARNING", "3"]]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
