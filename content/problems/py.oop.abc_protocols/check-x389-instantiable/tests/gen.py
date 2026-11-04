"""Inputs of check-x389-instantiable.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": [[["area", "perimeter"], ["area"], []]]}

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [[[]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["perimeter"]]], "tags": []},
    {"id": "h04", "args": [[["perimeter", "area"], ["area", "perimeter"]]], "tags": []},
    {"id": "h05", "args": [[["area"], ["perimeter"], ["area", "perimeter"]]], "tags": []},
    {"id": "h06", "args": [[[], [], ["area", "perimeter"], ["area"]]], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
