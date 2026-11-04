"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [["3", "2.5", "True", "abc"]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [[" 10 ", "-4", "false"]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [["abc", "xyz"]], "tags": []},
    {"id": "h03", "args": [["1", "2", "3"]], "tags": []},
    {"id": "h04", "args": [["1.5", "2.25"]], "tags": []},
    {"id": "h05", "args": [["TRUE", "False", "true"]], "tags": []},
    {"id": "h06", "args": [[" 7 ", "-3", " 0.5"]], "tags": []},
    {"id": "h07", "args": [["1e2", "3"]], "tags": []},
    {"id": "h08", "args": [["12abc", "", "  "]], "tags": []},
    {"id": "h09", "args": [["-2.5", "-2.5"]], "tags": []},
    {"id": "h10", "args": [["100", "0.1", "0.2"]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
