"""Inputs of check-x506 (class_ops); expected is recorded by tools/gen_hidden.py."""

SAMPLE = {
    "id": "s1",
    "ops": ["SnapshotArray", "set", "snap", "set", "snap", "get", "get"],
    "args": [[3], [0, 5], [], [0, 6], [], [0, 0], [0, 1]],
}

HIDDEN = [
    {"id": "h01", "ops": ["SnapshotArray", "get"], "args": [[1], [0, 0]], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["SnapshotArray", "snap", "snap", "get", "get"],
        "args": [[2], [], [], [1, 0], [0, 1]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["SnapshotArray", "set", "set", "snap", "get"],
        "args": [[2], [0, 1], [0, 2], [], [0, 0]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["SnapshotArray", "set", "snap", "snap", "set", "snap", "get", "get", "get"],
        "args": [[2], [1, 7], [], [], [1, 9], [], [1, 0], [1, 1], [1, 2]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["SnapshotArray", "snap", "set", "get", "snap", "get", "get"],
        "args": [[3], [], [2, 4], [2, 0], [], [2, 0], [2, 1]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["SnapshotArray", "set", "set", "snap", "set", "snap", "get", "get", "get", "get"],
        "args": [[3], [0, 1], [2, 3], [], [0, 8], [], [0, 0], [0, 1], [2, 1], [1, 1]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["SnapshotArray", "set", "snap", "set", "snap", "set", "snap", "get", "get", "get"],
        "args": [[1], [0, 1], [], [0, 0], [], [0, 5], [], [0, 0], [0, 1], [0, 2]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
