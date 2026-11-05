"""Inputs of check-x493-trie (class_ops). `expected` is recorded from solution.py."""

SAMPLE = {
    "id": "s1",
    "ops": ["Trie", "insert", "search", "search", "starts_with", "insert", "search"],
    "args": [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Trie", "search", "starts_with"],
        "args": [[], ["a"], ["a"]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["Trie", "insert", "search", "starts_with", "search"],
        "args": [[], ["a"], ["a"], ["a"], ["b"]],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Trie", "insert", "insert", "search", "search", "starts_with", "starts_with"],
        "args": [[], ["car"], ["cat"], ["ca"], ["cat"], ["ca"], ["cb"]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["Trie", "insert", "search", "starts_with", "search", "starts_with"],
        "args": [[], ["hello"], ["hell"], ["hell"], ["helloo"], ["helloo"]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["Trie", "insert", "insert", "insert", "search", "search", "search"],
        "args": [[], ["to"], ["tea"], ["ten"], ["te"], ["ten"], ["tex"]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["Trie", "insert", "insert", "search", "starts_with"],
        "args": [[], ["abc"], ["abc"], ["abc"], ["abcd"]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Trie", "insert", "starts_with", "search", "insert", "search"],
        "args": [[], ["zebra"], ["z"], ["z"], ["z"], ["z"]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
