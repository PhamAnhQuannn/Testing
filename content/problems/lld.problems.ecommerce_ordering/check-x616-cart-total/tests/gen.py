"""Inputs of check-x616-cart-total.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Cart", "add", "add", "subtotal", "set_discount", "total"],
    "args": [[], ["ao", 100, 2], ["non", 50, 1], [], ["percent10"], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Cart", "subtotal", "total", "set_discount", "total"],
        "args": [[], [], [], ["percent10"], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["Cart", "add", "add", "subtotal", "total"],
        "args": [[], ["ao", 100, 2], ["non", 50, 1], [], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Cart", "add", "set_discount", "total", "subtotal"],
        "args": [[], ["ao", 25, 3], ["percent10"], [], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["Cart", "add", "set_discount", "total", "subtotal"],
        "args": [[], ["non", 20, 2], ["fixed50"], [], []],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["Cart", "add", "set_discount", "total", "set_discount", "total"],
        "args": [[], ["ao", 99, 1], ["fixed50"], [], ["none"], []],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["Cart", "add", "add", "add", "set_discount", "total", "add", "total"],
        "args": [[], ["a", 7, 1], ["b", 13, 4], ["a", 7, 2], ["percent10"], [], ["c", 1000, 1], []],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["Cart", "add", "set_discount", "total", "set_discount", "total"],
        "args": [[], ["x", 50, 1], ["fixed50"], [], ["percent10"], []],
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
    kinds = ("none", "percent10", "fixed50")
    out = []
    for i in range(n):
        ops, args = ["Cart"], [[]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("add", "add", "set_discount", "subtotal", "total")[(state >> 16) % 5]
            ops.append(op)
            if op == "add":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                price = 1 + (state >> 16) % 120
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                qty = 1 + (state >> 16) % 4
                args.append([f"p{price}", price, qty])
            elif op == "set_discount":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([kinds[(state >> 16) % 3]])
            else:
                args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
