"""Hidden-test inputs for number-of-good-pairs; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [[1]], "tags": ["edge"]},
        {"id": "h02", "args": [[1, 1]], "tags": ["edge"]},
        {"id": "h03", "args": [[1, 2]], "tags": ["edge"]},
        {"id": "h04", "args": [[7, 7, 7, 7, 7]], "tags": ["all_equal"]},
        {"id": "h05", "args": [[1, 2, 3, 4, 5, 6]], "tags": ["all_distinct"]},
        {"id": "h06", "args": [[1, 2, 1, 2, 1, 2]], "tags": ["non_adjacent"]},
        {"id": "h07", "args": [[3, 1, 3, 1, 3, 3, 2, 2]], "tags": []},
        {"id": "h08", "args": [[100] * 100], "tags": ["max"]},
        {"id": "h09", "args": [[(i % 10) + 1 for i in range(100)]], "tags": ["max"]},
        {"id": "h10", "args": [list(range(1, 101))], "tags": ["max", "all_distinct"]},
        {"id": "h11", "args": [[5, 5, 9, 5, 9, 9]], "tags": []},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
