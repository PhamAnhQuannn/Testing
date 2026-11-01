"""Hidden-test inputs for fix-collect-evens; expected comes from solution.py.

Every case has at least two batches: the buggy shared default list leaks evens
from one batch into the next.
"""


def hidden_inputs():
    return [
        {"id": "h01", "args": [[[1, 2, 3, 4], [6, 8]]], "tags": ["state-leak"]},
        {"id": "h02", "args": [[[2], [4], [6]]], "tags": ["state-leak"]},
        {"id": "h03", "args": [[[1, 3], [5, 7]]], "tags": ["none"]},
        {"id": "h04", "args": [[[10, 11], [], [12]]], "tags": ["empty", "state-leak"]},
        {"id": "h05", "args": [[]], "tags": ["edge", "empty"]},
        {"id": "h06", "args": [[[0, -2, -3], [4, -6]]], "tags": ["state-leak"]},
        {"id": "h07", "args": [[[7], [8, 9], [10]]], "tags": ["state-leak"]},
    ]


def small_inputs(seed, n):
    return []
