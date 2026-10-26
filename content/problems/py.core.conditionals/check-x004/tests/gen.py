"""Hidden-test inputs for check-x004; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [1], "tags": ["edge"]},
        {"id": "h02", "args": [3], "tags": []},
        {"id": "h03", "args": [5], "tags": []},
        {"id": "h04", "args": [7], "tags": []},
        {"id": "h05", "args": [9], "tags": []},
        {"id": "h06", "args": [10], "tags": []},
        {"id": "h07", "args": [15], "tags": ["both"]},
        {"id": "h08", "args": [30], "tags": ["both"]},
        {"id": "h09", "args": [14], "tags": []},
        {"id": "h10", "args": [10000], "tags": ["max"]},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
