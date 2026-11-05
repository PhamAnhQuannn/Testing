"""Inputs of check-x494-word-dictionary (class_ops). `expected` is recorded from solution.py."""

SAMPLE = {
    "id": "s1",
    "ops": [
        "WordDictionary",
        "add_word",
        "add_word",
        "add_word",
        "search",
        "search",
        "search",
        "search",
    ],
    "args": [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["WordDictionary", "search", "search"],
        "args": [[], ["a"], ["."]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["WordDictionary", "add_word", "search", "search", "search"],
        "args": [[], ["a"], ["a"], ["."], ["b"]],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["WordDictionary", "add_word", "search", "search", "search", "search"],
        "args": [[], ["abc"], ["ab"], ["abcd"], ["..."], ["a.d"]],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["WordDictionary", "add_word", "add_word", "search", "search", "search", "search"],
        "args": [[], ["at"], ["and"], ["a"], ["an."], ["a.d."], ["...."]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["WordDictionary", "add_word", "add_word", "search", "search", "search", "search"],
        "args": [[], ["cat"], ["car"], ["ca."], ["c.r"], [".a."], ["c.t."]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["WordDictionary", "add_word", "search", "add_word", "search", "search"],
        "args": [[], ["dog"], ["do."], ["do"], ["do."], ["do"]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["WordDictionary", "add_word", "add_word", "search", "search", "search"],
        "args": [[], ["hello"], ["help"], ["hel.o"], ["hel.."], ["h.l.."]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
