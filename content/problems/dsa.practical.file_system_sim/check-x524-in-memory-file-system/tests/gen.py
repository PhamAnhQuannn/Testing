"""Inputs of check-x524-in-memory-file-system (class_ops).

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["FileSystem", "ls", "mkdir", "add_content_to_file", "ls", "read_content_from_file"],
    "args": [[], ["/"], ["/a/b/c"], ["/a/b/c/d", "hello"], ["/a/b/c"], ["/a/b/c/d"]],
}

HIDDEN = [
    {"id": "h01", "ops": ["FileSystem", "ls"], "args": [[], ["/"]], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["FileSystem", "mkdir", "ls", "ls"],
        "args": [[], ["/a/b"], ["/"], ["/a"]],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["FileSystem", "mkdir", "mkdir", "mkdir", "ls"],
        "args": [[], ["/z"], ["/m"], ["/b"], ["/"]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": [
            "FileSystem",
            "add_content_to_file",
            "add_content_to_file",
            "read_content_from_file",
        ],
        "args": [[], ["/f", "ab"], ["/f", "cd"], ["/f"]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["FileSystem", "add_content_to_file", "ls", "ls"],
        "args": [[], ["/x/y/file.txt", "hi"], ["/x/y/file.txt"], ["/x/y"]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": [
            "FileSystem",
            "mkdir",
            "add_content_to_file",
            "add_content_to_file",
            "ls",
            "read_content_from_file",
        ],
        "args": [[], ["/d"], ["/d/b", "1"], ["/d/a", "2"], ["/d"], ["/d/a"]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["FileSystem", "mkdir", "mkdir", "ls"],
        "args": [[], ["/a/b"], ["/a/b"], ["/a"]],
        "tags": ["edge"],
    },
    {
        "id": "h08",
        "ops": [
            "FileSystem",
            "add_content_to_file",
            "add_content_to_file",
            "add_content_to_file",
            "ls",
            "ls",
        ],
        "args": [[], ["/a/f", "x"], ["/a/g", "y"], ["/a/b/h", "z"], ["/a"], ["/"]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
