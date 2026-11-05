"""Inputs of check-x565-bank-account.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["BankAccount", "deposit", "withdraw", "balance"],
    "args": [[], [100], [30], []],
}

HIDDEN = [
    {"id": "h01", "ops": ["BankAccount", "balance"], "args": [[], []], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["BankAccount", "deposit", "deposit", "balance"],
        "args": [[], [40], [60], []],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["BankAccount", "deposit", "withdraw", "balance"],
        "args": [[], [50], [80], []],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["BankAccount", "deposit", "deposit", "withdraw", "balance"],
        "args": [[], [-5], [0], [10], []],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["BankAccount", "deposit", "withdraw", "withdraw", "balance"],
        "args": [[], [100], [-20], [0], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["BankAccount", "deposit", "withdraw", "balance", "withdraw", "balance"],
        "args": [[], [100], [100], [], [1], []],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": ["BankAccount", "deposit", "withdraw", "deposit", "withdraw", "balance"],
        "args": [[], [30], [10], [5], [26], []],
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
        ops, args = ["BankAccount"], [[]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = ("deposit", "withdraw", "balance")[(state >> 16) % 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            ops.append(kind)
            args.append([] if kind == "balance" else [((state >> 16) % 41) - 10])
        ops.append("balance")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
