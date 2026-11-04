"""Inputs of check-x377-mro-names; `expected` is recorded from solution.py by gen_hidden."""

DIAMOND = [["A", []], ["B", ["A"]], ["C", ["A"]], ["D", ["B", "C"]]]
BAD = [["X", []], ["Y", ["X"]], ["Z", ["X", "Y"]]]
CHAIN = [["A", []], ["B", ["A"]], ["C", ["B"]]]

SAMPLES = [
    {"id": "s1", "args": [DIAMOND]},
    {"id": "s2", "args": [CHAIN]},
    {"id": "s3", "args": [BAD]},
]

HIDDEN = [
    {"id": "h01", "args": [[["A", []]]], "tags": ["edge"]},
    {"id": "h02", "args": [BAD], "tags": ["edge"]},
    {"id": "h03", "args": [[["A", []], ["B", ["A"]], ["C", ["A"]], ["D", ["C", "B"]]]], "tags": []},
    {"id": "h04", "args": [[["A", []], ["B", []], ["C", ["A", "B"]]]], "tags": []},
    {"id": "h05", "args": [CHAIN + [["D", ["C"]]]], "tags": []},
    {
        "id": "h06",
        "args": [
            [
                ["O", []],
                ["A", ["O"]],
                ["B", ["O"]],
                ["C", ["O"]],
                ["D", ["A", "B"]],
                ["E", ["B", "C"]],
                ["F", ["D", "E"]],
            ]
        ],
        "tags": [],
    },
    {"id": "h07", "args": [[["A", []], ["B", ["A"]], ["C", ["A", "B"]]]], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
