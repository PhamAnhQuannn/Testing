"""Inputs of check-x586-editor-undo.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Editor", "type", "type", "undo", "text"],
    "args": [[], ["ab"], ["cd"], [], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Editor", "type", "type", "undo", "text"],
        "args": [[], ["ab"], ["cd"], [], []],
        "tags": [],
    },
    {
        "id": "h02",
        "ops": ["Editor", "type", "delete", "text", "undo", "text"],
        "args": [[], ["hello"], [2], [], [], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Editor", "type", "delete", "text", "undo", "text"],
        "args": [[], ["abc"], [10], [], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["Editor", "type", "type", "type", "undo", "undo", "text", "undo", "text"],
        "args": [[], ["a"], ["bc"], ["def"], [], [], [], [], []],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["Editor", "undo", "text", "type", "undo", "undo", "text"],
        "args": [[], [], [], ["x"], [], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["Editor", "text"],
        "args": [[], []],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": ["Editor", "delete", "undo", "type", "text", "undo", "text"],
        "args": [[], [3], [], ["ok"], [], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h08",
        "ops": [
            "Editor",
            "type",
            "delete",
            "delete",
            "text",
            "undo",
            "text",
            "undo",
            "text",
            "undo",
            "text",
        ],
        "args": [[], ["abcdef"], [4], [9], [], [], [], [], [], [], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic LCG op-sequences (no random module)."""
    state = seed & 0x7FFFFFFF
    out = []
    for i in range(n):
        ops, args = ["Editor"], [[]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = ("type", "delete", "undo", "text")[(state >> 16) % 4]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            ops.append(kind)
            if kind == "type":
                args.append(["abcde"[: (state >> 16) % 5 + 1]])
            elif kind == "delete":
                args.append([(state >> 16) % 6])
            else:
                args.append([])
        ops.append("text")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
