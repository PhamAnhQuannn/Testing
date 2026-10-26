"""Hidden-test inputs for ugly-number; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [1], "tags": ["edge"]},
        {"id": "h02", "args": [0], "tags": ["edge", "zero"]},
        {"id": "h03", "args": [-6], "tags": ["negative"]},
        {"id": "h04", "args": [6], "tags": []},
        {"id": "h05", "args": [8], "tags": []},
        {"id": "h06", "args": [14], "tags": []},
        {"id": "h07", "args": [30], "tags": []},
        {"id": "h08", "args": [7], "tags": ["prime"]},
        {"id": "h09", "args": [25], "tags": []},
        {"id": "h10", "args": [49], "tags": []},
        {"id": "h11", "args": [1073741824], "tags": ["max", "power_of_two"]},
        {"id": "h12", "args": [2147483647], "tags": ["max"]},
        {"id": "h13", "args": [-2147483648], "tags": ["max", "negative"]},
        {"id": "h14", "args": [1594323], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
