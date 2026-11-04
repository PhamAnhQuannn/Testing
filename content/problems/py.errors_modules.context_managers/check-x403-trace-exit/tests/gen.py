"""Inputs of check-x403-trace-exit; `expected` is recorded from solution.py."""

SAMPLE = {"id": "s1", "args": ["value"]}

HIDDEN = [
    {"id": "h01", "args": ["ok"], "tags": []},
    {"id": "h02", "args": ["value"], "tags": []},
    {"id": "h03", "args": ["key"], "tags": ["edge"]},
    {"id": "h04", "args": ["other"], "tags": ["edge"]},
    {"id": "h05", "args": [""], "tags": ["edge"]},
    {"id": "h06", "args": ["VALUE"], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []
