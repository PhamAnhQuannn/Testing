"""Inputs of check-x583-cart-discount.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Cart", "add", "add", "set_discount", "total"],
    "args": [[], [100], [100], ["percent10"], []],
}

HIDDEN = [
    {"id": "h01", "ops": ["Cart", "total"], "args": [[], []], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["Cart", "add", "add", "total"],
        "args": [[], [30], [45], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Cart", "add", "set_discount", "total"],
        "args": [[], [250], ["percent10"], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["Cart", "add", "set_discount", "total"],
        "args": [[], [250], ["fixed50"], []],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["Cart", "add", "set_discount", "total"],
        "args": [[], [20], ["fixed50"], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["Cart", "set_discount", "total"],
        "args": [[], ["fixed50"], []],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": [
            "Cart",
            "add",
            "set_discount",
            "total",
            "set_discount",
            "total",
            "set_discount",
            "total",
        ],
        "args": [[], [99], ["percent10"], [], ["fixed50"], [], ["none"], []],
        "tags": [],
    },
    {
        "id": "h08",
        "ops": ["Cart", "set_discount", "add", "add", "total", "add", "total"],
        "args": [[], ["percent10"], [15], [16], [], [1000], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic LCG op-sequences (no random module)."""
    kinds = ("none", "percent10", "fixed50")
    state = seed & 0x7FFFFFFF
    out = []
    for i in range(n):
        ops, args = ["Cart"], [[]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("add", "set_discount", "total")[(state >> 16) % 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            ops.append(op)
            if op == "total":
                args.append([])
            elif op == "add":
                args.append([(state >> 16) % 120])
            else:
                args.append([kinds[(state >> 16) % 3]])
        ops.append("total")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
