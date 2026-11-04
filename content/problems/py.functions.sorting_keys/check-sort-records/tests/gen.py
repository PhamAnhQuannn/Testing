"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {
        "id": "s1",
        "args": [
            [["an", "eng", 30, 80], ["binh", "ops", 25, 90], ["chi", "eng", 25, 90]],
            ["name"],
        ],
    },
    {
        "id": "s2",
        "args": [
            [["an", "eng", 30, 80], ["binh", "ops", 25, 90], ["chi", "eng", 25, 90]],
            ["-score", "name"],
        ],
    },
    {
        "id": "s3",
        "args": [
            [["an", "eng", 30, 80], ["binh", "ops", 25, 90], ["chi", "eng", 25, 90]],
            ["dept", "-age"],
        ],
    },
]

HIDDEN = [
    {"id": "h01", "args": [[], ["name"]], "tags": ["edge"]},
    {
        "id": "h02",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            [],
        ],
        "tags": [],
    },
    {
        "id": "h03",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["name"],
        ],
        "tags": [],
    },
    {
        "id": "h04",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["-score"],
        ],
        "tags": [],
    },
    {
        "id": "h05",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["dept", "-score"],
        ],
        "tags": [],
    },
    {
        "id": "h06",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["-score", "age", "name"],
        ],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["age", "-dept"],
        ],
        "tags": [],
    },
    {
        "id": "h08",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["-dept", "-age", "-name"],
        ],
        "tags": [],
    },
    {
        "id": "h09",
        "args": [
            [
                ["an", "eng", 30, 80],
                ["binh", "ops", 25, 90],
                ["chi", "eng", 25, 90],
                ["dung", "ops", 41, 70],
                ["em", "eng", 30, 95],
                ["phuc", "hr", 25, 70],
                ["giang", "hr", 30, 80],
            ],
            ["score", "-age"],
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
