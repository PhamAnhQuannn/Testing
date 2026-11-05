"""Inputs of check-x525-file-search (class_ops).

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["FileStore", "add_file", "add_file", "add_file", "total_size", "find_by_min_size"],
    "args": [[], ["/a/x.txt", 10], ["/a/b/y.txt", 30], ["/c/z.txt", 5], ["/a"], ["/a", 20]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["FileStore", "total_size", "find_by_min_size"],
        "args": [[], ["/"], ["/", 0]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["FileStore", "add_file", "add_file", "total_size", "total_size"],
        "args": [[], ["/a/f", 3], ["/a/b/g", 4], ["/a"], ["/a/b"]],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["FileStore", "add_file", "add_file", "add_file", "find_by_min_size"],
        "args": [[], ["/d/b", 5], ["/d/a", 5], ["/d/c", 1], ["/d", 5]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["FileStore", "add_file", "find_by_min_size", "total_size"],
        "args": [[], ["/a/f", 3], ["/a", 100], ["/a"]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["FileStore", "add_file", "add_file", "total_size", "total_size"],
        "args": [[], ["/ab/f", 7], ["/a/f", 2], ["/a"], ["/ab"]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["FileStore", "add_file", "add_file", "total_size"],
        "args": [[], ["/a/f", 3], ["/a/f", 9], ["/"]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": [
            "FileStore",
            "add_file",
            "add_file",
            "add_file",
            "find_by_min_size",
            "find_by_min_size",
        ],
        "args": [[], ["/r/z/1", 50], ["/r/a/2", 60], ["/q", 70], ["/", 55], ["/r", 0]],
        "tags": [],
    },
    {
        "id": "h08",
        "ops": ["FileStore", "add_file", "total_size", "total_size"],
        "args": [[], ["/deep/a/b/c/d.bin", 1000], ["/deep/a"], ["/nothing"]],
        "tags": ["edge"],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
