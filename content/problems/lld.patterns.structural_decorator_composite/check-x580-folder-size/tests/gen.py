"""Inputs of check-x580-folder-size; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [["folder", "root", [["file", "a", 10], ["folder", "sub", [["file", "b", 5]]]]]],
    },
    {"id": "s2", "args": [["file", "x", 7]]},
]


def _tree(x, depth):
    """Build a shallow tree from LCG state x; returns (node, new_x)."""
    x = (x * 1103515245 + 12345) % 2147483648
    pick = (x >> 8) % 4
    if depth == 0 or pick < 2:
        x = (x * 1103515245 + 12345) % 2147483648
        return ["file", f"f{(x >> 8) % 100}", (x >> 8) % 1000], x
    count = (x >> 12) % 4
    children = []
    for _ in range(count):
        child, x = _tree(x, depth - 1)
        children.append(child)
    return ["folder", f"d{(x >> 8) % 100}", children], x


def _lcg_tree(seed, depth):
    node, _ = _tree(seed, depth)
    return node


HIDDEN = [
    {"id": "h01", "args": [["folder", "empty", []]], "tags": ["edge"]},
    {"id": "h02", "args": [["file", "solo", 42]], "tags": ["edge"]},
    {"id": "h03", "args": [["file", "zero", 0]], "tags": ["zero"]},
    {
        "id": "h04",
        "args": [["folder", "r", [["file", "a", 1], ["file", "b", 2], ["file", "c", 3]]]],
        "tags": ["flat"],
    },
    {
        "id": "h05",
        "args": [["folder", "r", [["folder", "e1", []], ["folder", "e2", [["folder", "e3", []]]]]]],
        "tags": ["empty-nested"],
    },
    {
        "id": "h06",
        "args": [
            [
                "folder",
                "root",
                [
                    ["file", "a", 100000],
                    ["folder", "x", [["file", "b", 20], ["folder", "y", [["file", "c", 3]]]]],
                    ["folder", "z", [["file", "d", 4000]]],
                ],
            ]
        ],
        "tags": ["nested"],
    },
    {
        "id": "h07",
        "args": [
            [
                "folder",
                "l1",
                [
                    [
                        "folder",
                        "l2",
                        [
                            [
                                "folder",
                                "l3",
                                [
                                    [
                                        "folder",
                                        "l4",
                                        [
                                            [
                                                "folder",
                                                "l5",
                                                [["file", "deep", 9], ["file", "deeper", 11]],
                                            ]
                                        ],
                                    ]
                                ],
                            ]
                        ],
                    ]
                ],
            ]
        ],
        "tags": ["deep"],
    },
    {"id": "h08", "args": [_lcg_tree(3, 4)], "tags": []},
    {"id": "h09", "args": [_lcg_tree(11, 5)], "tags": []},
    {"id": "h10", "args": [_lcg_tree(29, 4)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": [_lcg_tree(seed * 1000 + i + 1, 3)]} for i in range(n)]
