"""Inputs of check-x592-requirement-spec.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["RequirementSpec", "add", "add", "set_scope", "set_scope", "count", "in_scope"],
    "args": [
        [],
        ["functional", "login"],
        ["nonfunctional", "fast"],
        ["payments", False],
        ["search", True],
        ["functional"],
        [],
    ],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["RequirementSpec", "count", "count", "in_scope"],
        "args": [[], ["functional"], ["nonfunctional"], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["RequirementSpec", "add", "add", "add", "count", "count"],
        "args": [
            [],
            ["functional", "a"],
            ["functional", "b"],
            ["functional", "a"],
            ["functional"],
            ["nonfunctional"],
        ],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["RequirementSpec", "add", "add", "count", "count"],
        "args": [
            [],
            ["nonfunctional", "p95"],
            ["nonfunctional", "uptime"],
            ["functional"],
            ["nonfunctional"],
        ],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["RequirementSpec", "add", "add", "add", "count", "count"],
        "args": [
            [],
            ["functional", "x"],
            ["nonfunctional", "y"],
            ["functional", "z"],
            ["functional"],
            ["nonfunctional"],
        ],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["RequirementSpec", "set_scope", "set_scope", "set_scope", "in_scope"],
        "args": [[], ["zeta", True], ["camera", False], ["alpha", True], []],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["RequirementSpec", "set_scope", "set_scope", "in_scope", "count"],
        "args": [[], ["camera", False], ["payments", False], [], ["functional"]],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": ["RequirementSpec", "add", "set_scope", "in_scope", "set_scope", "in_scope"],
        "args": [[], ["functional", "park"], ["fees", True], [], ["bay", True], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic LCG op-sequences (no random module)."""
    kinds = ("functional", "nonfunctional")
    names = ("login", "search", "fast", "pay", "report", "audit")
    state = seed & 0x7FFFFFFF
    out = []
    for i in range(n):
        ops, args = ["RequirementSpec"], [[]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("add", "set_scope", "count", "in_scope")[(state >> 16) & 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            pick = state >> 16
            ops.append(op)
            if op == "add":
                args.append([kinds[pick & 1], names[(pick >> 1) % 6]])
            elif op == "set_scope":
                args.append([names[(pick >> 1) % 6], bool(pick & 1)])
            elif op == "count":
                args.append([kinds[pick & 1]])
            else:
                args.append([])
        ops.append("in_scope")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
