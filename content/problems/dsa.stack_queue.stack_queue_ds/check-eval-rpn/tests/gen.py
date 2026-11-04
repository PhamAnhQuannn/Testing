"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [["2", "1", "+", "3", "*"]]},
    {"id": "s2", "args": [["4", "13", "5", "/", "+"]]},
    {"id": "s3", "args": [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]]},
]
HIDDEN = [
    {"id": "h01", "args": [["5"]], "tags": ["edge"]},
    {"id": "h02", "args": [["3", "4", "-"]], "tags": []},
    {"id": "h03", "args": [["7", "-2", "/"]], "tags": []},
    {"id": "h04", "args": [["-7", "2", "/"]], "tags": []},
    {"id": "h05", "args": [["2", "3", "*", "4", "5", "*", "+"]], "tags": []},
    {"id": "h06", "args": [["0", "3", "-"]], "tags": []},
    {"id": "h07", "args": [["100", "10", "/", "5", "/"]], "tags": []},
    {"id": "h08", "args": [["1", "2", "3", "4", "+", "+", "+"]], "tags": []},
    {"id": "h09", "args": [["-3", "-4", "*"]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
