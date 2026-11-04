"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": ["abcabcbb"]},
    {"id": "s2", "args": ["bbbbb"]},
    {"id": "s3", "args": ["pwwkew"]},
]
HIDDEN = [
    {"id": "h01", "args": [""], "tags": ["edge"]},
    {"id": "h02", "args": ["a"], "tags": []},
    {"id": "h03", "args": ["abcdef"], "tags": []},
    {"id": "h04", "args": ["abba"], "tags": []},
    {"id": "h05", "args": ["dvdf"], "tags": []},
    {"id": "h06", "args": ["tmmzuxt"], "tags": []},
    {"id": "h07", "args": ["aab"], "tags": []},
    {"id": "h08", "args": ["ab ab cd"], "tags": []},
    {"id": "h09", "args": ["aAbB"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
