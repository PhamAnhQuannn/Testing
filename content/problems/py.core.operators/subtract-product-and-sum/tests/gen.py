"""Hidden-test inputs for subtract-product-and-sum; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [1], "tags": ["edge"]},
        {"id": "h02", "args": [10], "tags": ["zero_digit"]},
        {"id": "h03", "args": [100000], "tags": ["max", "zero_digit"]},
        {"id": "h04", "args": [99999], "tags": ["max"]},
        {"id": "h05", "args": [7], "tags": ["single_digit"]},
        {"id": "h06", "args": [11], "tags": []},
        {"id": "h07", "args": [505], "tags": ["zero_digit"]},
        {"id": "h08", "args": [12345], "tags": []},
        {"id": "h09", "args": [90909], "tags": ["zero_digit"]},
        {"id": "h10", "args": [9], "tags": ["single_digit"]},
        {"id": "h11", "args": [88], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
