"""Inputs of check-x507 (class_ops); expected is recorded by tools/gen_hidden.py."""

SAMPLE = {
    "id": "s1",
    "ops": ["HitCounter", "hit", "hit", "hit", "get_hits", "hit", "get_hits", "get_hits"],
    "args": [[], [1], [2], [3], [4], [300], [300], [301]],
}

HIDDEN = [
    {"id": "h01", "ops": ["HitCounter", "get_hits"], "args": [[], [10]], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["HitCounter", "hit", "get_hits", "get_hits", "get_hits"],
        "args": [[], [1], [300], [301], [302]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["HitCounter", "hit", "hit", "hit", "get_hits"],
        "args": [[], [5], [5], [5], [5]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["HitCounter", "hit", "hit", "get_hits", "get_hits", "hit", "get_hits"],
        "args": [[], [100], [250], [350], [400], [500], [600]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["HitCounter", "hit", "get_hits", "hit", "get_hits", "get_hits"],
        "args": [[], [1], [1], [2], [2], [3]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["HitCounter", "hit", "hit", "hit", "hit", "get_hits", "get_hits", "get_hits"],
        "args": [[], [1], [100], [200], [300], [300], [399], [600]],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
