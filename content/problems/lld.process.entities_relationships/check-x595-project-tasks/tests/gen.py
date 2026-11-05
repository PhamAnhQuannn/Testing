"""Inputs of check-x595-project-tasks.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Project", "add_task", "add_task", "complete", "pending", "done_names"],
    "args": [["p1"], ["a"], ["b"], ["a"], [], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Project", "pending", "done_names"],
        "args": [["e"], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["Project", "add_task", "add_task", "pending"],
        "args": [["p"], ["a"], ["a"], []],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["Project", "add_task", "complete", "add_task", "pending", "done_names"],
        "args": [["p"], ["a"], ["a"], ["a"], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["Project", "add_task", "complete", "pending", "done_names"],
        "args": [["p"], ["a"], ["zzz"], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["Project", "add_task", "complete", "complete", "pending", "done_names"],
        "args": [["p"], ["a"], ["a"], ["a"], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": [
            "Project",
            "add_task",
            "add_task",
            "add_task",
            "complete",
            "complete",
            "complete",
            "pending",
            "done_names",
        ],
        "args": [["p"], ["c"], ["a"], ["b"], ["b"], ["c"], ["a"], [], []],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": [
            "Project",
            "add_task",
            "add_task",
            "complete",
            "pending",
            "add_task",
            "pending",
            "done_names",
        ],
        "args": [["p"], ["x"], ["y"], ["y"], [], ["z"], [], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic LCG op-sequences (no random module)."""
    names = ("a", "b", "c", "d")
    state = seed & 0x7FFFFFFF
    out = []
    for i in range(n):
        ops, args = ["Project"], [[f"p{i}"]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("add_task", "complete", "pending", "done_names")[(state >> 16) & 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            ops.append(op)
            if op in ("add_task", "complete"):
                args.append([names[(state >> 16) & 3]])
            else:
                args.append([])
        ops.append("pending")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
