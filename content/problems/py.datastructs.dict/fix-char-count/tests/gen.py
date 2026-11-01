"""Hidden-test inputs for fix-char-count; expected comes from solution.py."""


def hidden_inputs():
    return [
        {"id": "h01", "args": [""], "tags": ["empty"]},
        {"id": "h02", "args": ["a"], "tags": ["edge"]},
        {"id": "h03", "args": ["aa"], "tags": ["edge"]},
        {"id": "h04", "args": ["abc"], "tags": []},
        {"id": "h05", "args": ["banana"], "tags": []},
        {"id": "h06", "args": ["mississippi"], "tags": []},
        {"id": "h07", "args": ["Hello, World!"], "tags": []},
        {"id": "h08", "args": ["z" * 40], "tags": ["edge"]},
    ]


def small_inputs(seed, n):
    return []
