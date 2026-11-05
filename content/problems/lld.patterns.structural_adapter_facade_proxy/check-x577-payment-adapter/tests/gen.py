"""Inputs of check-x577-payment-adapter.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["PaymentAdapter", "pay", "pay", "total_cents"],
    "args": [[], [25], [10], []],
}

HIDDEN = [
    {"id": "h01", "ops": ["PaymentAdapter", "total_cents"], "args": [[], []], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["PaymentAdapter", "pay", "total_cents"],
        "args": [[], [25], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["PaymentAdapter", "pay", "pay", "pay", "total_cents"],
        "args": [[], [1], [20], [300], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["PaymentAdapter", "pay", "refund", "total_cents"],
        "args": [[], [50], [20], []],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["PaymentAdapter", "pay", "refund", "total_cents"],
        "args": [[], [10], [30], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["PaymentAdapter", "refund", "pay", "total_cents"],
        "args": [[], [5], [7], []],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": [
            "PaymentAdapter",
            "pay",
            "total_cents",
            "refund",
            "pay",
            "total_cents",
            "refund",
            "total_cents",
        ],
        "args": [[], [12], [], [4], [3], [], [100], []],
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
        ops, args = ["PaymentAdapter"], [[]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = ("pay", "refund", "total_cents")[(state >> 16) % 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            ops.append(kind)
            args.append([] if kind == "total_cents" else [(state >> 16) % 40])
        ops.append("total_cents")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
