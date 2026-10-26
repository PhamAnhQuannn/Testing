"""Hidden-test inputs for check-x002; tools/gen_hidden.py computes `expected` from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [0, "0"], "tags": ["edge"]},
        {"id": "h02", "args": [5, "10"], "tags": []},
        {"id": "h03", "args": [-7, "3"], "tags": ["negative"]},
        {"id": "h04", "args": [4, "-9"], "tags": ["negative"]},
        {"id": "h05", "args": [12, "007"], "tags": ["leading_zero"]},
        {"id": "h06", "args": [1000, "1000"], "tags": ["edge"]},
        {"id": "h07", "args": [-1000, "-1000"], "tags": ["edge"]},
        {"id": "h08", "args": [99, "1"], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
