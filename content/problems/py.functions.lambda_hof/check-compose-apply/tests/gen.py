"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3], [["add", 1], ["mul", 2]]]},
    {"id": "s2", "args": [[1, 2, 3], [["mul", 2], ["add", 1]]]},
    {"id": "s3", "args": [[-2, 0, 5], [["pow", 2], ["add", 3]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [["add", 1]]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3], []], "tags": []},
    {"id": "h03", "args": [[1, 2, 3], [["add", 1], ["mul", 2]]], "tags": []},
    {"id": "h04", "args": [[1, 2, 3], [["mul", 2], ["add", 1]]], "tags": []},
    {"id": "h05", "args": [[-2, 0, 5], [["pow", 2], ["add", 3]]], "tags": []},
    {"id": "h06", "args": [[7, 8, 9], [["mod", 5], ["neg", 0]]], "tags": []},
    {"id": "h07", "args": [[1, 2, 3, 4], [["add", 1], ["add", 2], ["add", 3]]], "tags": []},
    {"id": "h08", "args": [[3, -3], [["neg", 0], ["pow", 3], ["mod", 7], ["mul", 4]]], "tags": []},
    {
        "id": "h09",
        "args": [[10, 20], [["mul", 3], ["mod", 8], ["pow", 2], ["add", -1]]],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
