"""Hidden-test inputs for check-x008; tools/gen_hidden.py computes `expected` from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [5, []], "tags": ["edge", "empty"]},
        {"id": "h02", "args": [3, ["inc", "double"]], "tags": []},
        {"id": "h03", "args": [3, ["double", "inc"]], "tags": ["order"]},
        {"id": "h04", "args": [-4, ["square"]], "tags": ["negative"]},
        {"id": "h05", "args": [7, ["neg", "neg"]], "tags": []},
        {"id": "h06", "args": [0, ["inc", "inc", "square", "neg"]], "tags": []},
        {"id": "h07", "args": [2, ["square", "square", "double", "inc", "neg", "inc"]], "tags": []},
        {"id": "h08", "args": [-100, ["neg", "double", "inc"]], "tags": ["extremes"]},
    ]


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
