"""Inputs of check-x610-elevator-scan.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Elevator", "request", "request", "request", "step", "step", "step"],
    "args": [[3], [5], [1], [7], [], [], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Elevator", "request", "step", "current", "pending"],
        "args": [[0], [4], [], [], []],
        "tags": [],
    },
    {
        "id": "h02",
        "ops": ["Elevator", "request", "request", "request", "step", "step", "step", "pending"],
        "args": [[3], [5], [1], [7], [], [], [], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Elevator", "request", "request", "step", "step", "current"],
        "args": [[8], [2], [5], [], [], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["Elevator", "step", "step", "current", "pending"],
        "args": [[4], [], [], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": [
            "Elevator",
            "request",
            "request",
            "request",
            "request",
            "pending",
            "step",
            "pending",
        ],
        "args": [[2], [6], [6], [2], [6], [], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": [
            "Elevator",
            "request",
            "request",
            "request",
            "step",
            "request",
            "request",
            "step",
            "step",
            "step",
            "step",
            "step",
        ],
        "args": [[5], [3], [9], [7], [], [8], [1], [], [], [], [], []],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Elevator", "request", "step", "request", "step", "request", "step", "current"],
        "args": [[5], [2], [], [6], [], [4], [], []],
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
    out = []
    for i in range(n):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        ops, args = ["Elevator"], [[(state >> 16) % 10]]
        for _ in range(12):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = ("request", "request", "step", "current", "pending")[(state >> 16) % 5]
            ops.append(kind)
            if kind == "request":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([(state >> 16) % 10])
            else:
                args.append([])
        ops.append("pending")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
