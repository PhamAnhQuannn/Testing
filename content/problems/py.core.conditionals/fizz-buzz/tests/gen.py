"""Hidden-test inputs for fizz-buzz; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [1], "tags": ["edge"]},
        {"id": "h02", "args": [2], "tags": []},
        {"id": "h03", "args": [3], "tags": []},
        {"id": "h04", "args": [5], "tags": []},
        {"id": "h05", "args": [15], "tags": ["fizzbuzz"]},
        {"id": "h06", "args": [16], "tags": []},
        {"id": "h07", "args": [30], "tags": ["fizzbuzz"]},
        {"id": "h08", "args": [100], "tags": []},
        {"id": "h09", "args": [1000], "tags": []},
        {"id": "h10", "args": [10000], "tags": ["max"]},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
