"""Inputs of check-x362-parse-ints; expected is recorded from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [["1", "x", " 3 ", "4.5"]]},
    {"id": "s2", "args": [["10", "20", "30"]]},
    {"id": "s3", "args": [["a", "b", ""]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [["-5", "+7", "0", "007"]], "tags": []},
    {"id": "h03", "args": [["1e3", "0x10", "1_000", "12"]], "tags": []},
    {"id": "h04", "args": [["", " ", "  9  "]], "tags": []},
    {"id": "h05", "args": [["3", "three", "3.0", "-3"]], "tags": []},
    {"id": "h06", "args": [["--1", "-", "+", "5"]], "tags": []},
    {"id": "h07", "args": [["99999999999999999999", "x"]], "tags": []},
    {"id": "h08", "args": [["x", "y", "z"]], "tags": []},
    {"id": "h09", "args": [["8", "8", "x", "8"]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
