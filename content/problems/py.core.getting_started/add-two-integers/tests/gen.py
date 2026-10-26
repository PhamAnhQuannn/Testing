"""Hidden-test inputs for add-two-integers; gen_hidden.py computes `expected` from solution.py."""

LOW, HIGH = -100, 100


def hidden_inputs():
    return [
        {"id": "h01", "args": [0, 0], "tags": ["edge"]},
        {"id": "h02", "args": [HIGH, HIGH], "tags": ["edge"]},
        {"id": "h03", "args": [LOW, LOW], "tags": ["edge"]},
        {"id": "h04", "args": [LOW, HIGH], "tags": ["edge"]},
        {"id": "h05", "args": [-1, -1], "tags": ["negative"]},
        {"id": "h06", "args": [7, 0], "tags": ["zero"]},
        {"id": "h07", "args": [0, -7], "tags": ["zero"]},
        {"id": "h08", "args": [-3, 8], "tags": ["negative"]},
        {"id": "h09", "args": [5, -9], "tags": ["negative"]},
        {"id": "h10", "args": [41, 59], "tags": []},
        {"id": "h11", "args": [-64, -36], "tags": ["negative"]},
        {"id": "h12", "args": [1, 2], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
