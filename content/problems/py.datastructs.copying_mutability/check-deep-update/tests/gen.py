"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 2], [3, 4]], [[0, 1, 9], [1, 0, 7]]]},
    {"id": "s2", "args": [[[1]], [[0, 0, 5], [0, 0, 6]]]},
    {"id": "s3", "args": [[[0, 0], [0, 0]], []]},
]

HIDDEN = [
    {"id": "h01", "args": [[[1, 2], [3, 4]], [[0, 1, 9], [1, 0, 7]]], "tags": ["edge"]},
    {"id": "h02", "args": [[], []], "tags": []},
    {"id": "h03", "args": [[[1]], []], "tags": []},
    {"id": "h04", "args": [[[1]], [[0, 0, 5], [0, 0, 6]]], "tags": []},
    {"id": "h05", "args": [[[0, 0, 0], [0, 0, 0]], [[0, 0, 1], [1, 2, 2]]], "tags": []},
    {"id": "h06", "args": [[[5, 5]], [[0, 0, -1], [0, 1, -2]]], "tags": []},
    {"id": "h07", "args": [[[1, 2], [1, 2]], [[0, 0, 0]]], "tags": []},
    {
        "id": "h08",
        "args": [
            [[7, 8, 7, 7], [8, 9, 3, 2], [8, 7, 9, 2], [1, 7, 4, 2], [1, 8, 0, 9], [6, 7, 9, 2]],
            [
                [4, 0, 7],
                [0, 0, -8],
                [1, 1, -9],
                [3, 2, 5],
                [4, 1, 7],
                [1, 2, 6],
                [0, 0, 5],
                [5, 2, 4],
                [4, 0, -1],
                [2, 1, 7],
                [2, 0, -7],
                [4, 0, 3],
            ],
        ],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
