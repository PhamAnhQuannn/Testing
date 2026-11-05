"""Inputs of check-x598-library-api.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Library", "add_book", "borrow", "borrow", "available"],
    "args": [[], ["dune", 1], ["dune"], ["dune"], ["dune"]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Library", "add_book", "borrow", "borrow", "available"],
        "args": [[], ["dune", 1], ["dune"], ["dune"], ["dune"]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["Library", "return_book", "available", "borrow"],
        "args": [[], ["ghost"], ["ghost"], ["ghost"]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["Library", "add_book", "add_book", "available", "add_book", "available"],
        "args": [[], ["a", 2], ["a", 3], ["a"], ["b", 0], ["b"]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": [
            "Library",
            "add_book",
            "borrow",
            "borrow",
            "available",
            "return_book",
            "available",
            "return_book",
            "return_book",
            "available",
        ],
        "args": [[], ["x", 2], ["x"], ["x"], ["x"], ["x"], ["x"], ["x"], ["x"], ["x"]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["Library", "available", "available"],
        "args": [[], ["nope"], ["other"]],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": [
            "Library",
            "add_book",
            "add_book",
            "borrow",
            "borrow",
            "borrow",
            "available",
            "return_book",
            "borrow",
        ],
        "args": [[], ["p", 1], ["q", 1], ["p"], ["q"], ["p"], ["p"], ["q"], ["q"]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Library", "add_book", "return_book", "borrow", "add_book", "borrow", "available"],
        "args": [[], ["z", 0], ["z"], ["z"], ["z", 1], ["z"], ["z"]],
        "tags": ["edge"],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic LCG op-sequences (no random module)."""
    state = seed & 0x7FFFFFFF
    titles = ("a", "b", "c")
    out = []
    for i in range(n):
        ops, args = ["Library"], [[]]
        for _ in range(10):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = ("add_book", "borrow", "return_book", "available")[(state >> 16) % 4]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            title = titles[(state >> 16) % 3]
            ops.append(kind)
            if kind == "add_book":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([title, (state >> 16) % 4])
            else:
                args.append([title])
        ops.append("available")
        args.append(["a"])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
