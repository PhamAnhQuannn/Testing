"""Hidden-test inputs for check-x001; tools/gen_hidden.py computes `expected` from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [0, 10], "tags": ["edge"]},
        {"id": "h02", "args": [20, 10], "tags": ["edge"]},
        {"id": "h03", "args": [21, 10], "tags": ["edge"]},
        {"id": "h04", "args": [1, 1000], "tags": ["edge"]},
        {"id": "h05", "args": [7, 1], "tags": []},
        {"id": "h06", "args": [999, 1000], "tags": []},
        {"id": "h07", "args": [1000000, 7], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
