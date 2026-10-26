"""Hidden-test inputs for length-of-last-word; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": ["a"], "tags": ["edge"]},
        {"id": "h02", "args": ["a "], "tags": ["trailing_space"]},
        {"id": "h03", "args": ["  a"], "tags": ["leading_space"]},
        {"id": "h04", "args": ["Hello World"], "tags": []},
        {"id": "h05", "args": ["   fly me   to   the moon  "], "tags": ["spaces"]},
        {"id": "h06", "args": ["luffy is still joyboy"], "tags": []},
        {"id": "h07", "args": ["day"], "tags": ["one_word"]},
        {"id": "h08", "args": ["hello   "], "tags": ["trailing_space"]},
        {"id": "h09", "args": ["   hello"], "tags": ["leading_space"]},
        {"id": "h10", "args": ["a b c d e f"], "tags": []},
        {"id": "h11", "args": ["x" * 10000], "tags": ["max"]},
        {"id": "h12", "args": ["ab " * 3333 + "z"], "tags": ["max"]},
    ]


def small_inputs(seed, n):
    return []  # difficulty easy: no brute.py, so the cross-check is skipped
