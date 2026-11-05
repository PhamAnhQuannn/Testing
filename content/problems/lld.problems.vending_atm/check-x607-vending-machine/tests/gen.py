"""Inputs of check-x607-vending-machine.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["VendingMachine", "load", "insert", "select", "balance"],
    "args": [[], ["A1", 2, 10], [25], ["A1"], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["VendingMachine", "balance", "select"],
        "args": [[], [], ["A1"]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["VendingMachine", "load", "insert", "select", "select", "balance"],
        "args": [[], ["A1", 1, 10], [30], ["A1"], ["A1"], []],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["VendingMachine", "load", "insert", "select", "balance"],
        "args": [[], ["B2", 3, 15], [10], ["B2"], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["VendingMachine", "load", "insert", "select", "balance"],
        "args": [[], ["B2", 3, 15], [15], ["B2"], []],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["VendingMachine", "load", "insert", "select", "balance"],
        "args": [[], ["A1", 2, 10], [50], ["Z9"], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["VendingMachine", "load", "load", "insert", "select", "select", "balance"],
        "args": [[], ["A1", 0, 10], ["A1", 2, 20], [45], ["A1"], ["A1"], []],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": [
            "VendingMachine",
            "load",
            "insert",
            "select",
            "insert",
            "select",
            "balance",
        ],
        "args": [[], ["A1", 2, 10], [4], ["A1"], [6], ["A1"], []],
        "tags": [],
    },
    {
        "id": "h08",
        "ops": [
            "VendingMachine",
            "load",
            "load",
            "insert",
            "select",
            "select",
            "select",
            "balance",
        ],
        "args": [[], ["A1", 1, 5], ["B2", 1, 8], [20], ["B2"], ["A1"], ["A1"], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic LCG op-sequences (no random module)."""
    codes = ("A1", "B2", "C3")
    state = seed & 0x7FFFFFFF
    out = []
    for i in range(n):
        ops, args = ["VendingMachine"], [[]]
        for _ in range(10):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("load", "insert", "select", "select", "balance")[(state >> 16) % 5]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            pick = state >> 16
            ops.append(op)
            if op == "load":
                args.append([codes[pick % 3], (pick >> 2) % 3, 5 + (pick >> 4) % 20])
            elif op == "insert":
                args.append([(pick % 30)])
            elif op == "select":
                args.append([codes[pick % 3]])
            else:
                args.append([])
        ops.append("balance")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
