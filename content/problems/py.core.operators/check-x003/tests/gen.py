"""Hidden-test inputs for check-x003; tools/gen_hidden.py computes `expected` from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [0], "tags": ["edge"]},
        {"id": "h02", "args": [59], "tags": ["edge"]},
        {"id": "h03", "args": [60], "tags": ["edge"]},
        {"id": "h04", "args": [3599], "tags": ["edge"]},
        {"id": "h05", "args": [3600], "tags": ["edge"]},
        {"id": "h06", "args": [3661], "tags": []},
        {"id": "h07", "args": [86399], "tags": ["edge"]},
        {"id": "h08", "args": [100000], "tags": ["max"]},
        {"id": "h09", "args": [7325], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
