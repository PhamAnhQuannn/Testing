"""Inputs of check-x628-optimistic-seat.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["SeatStore", "add", "book", "book", "is_booked", "version"],
    "args": [[], ["a1"], ["a1", 0], ["a1", 0], ["a1"], ["a1"]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["SeatStore", "add", "book", "book", "is_booked", "version"],
        "args": [[], ["a1"], ["a1", 0], ["a1", 0], ["a1"], ["a1"]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["SeatStore", "add", "book", "is_booked", "version"],
        "args": [[], ["b2"], ["b2", 5], ["b2"], ["b2"]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["SeatStore", "book", "version", "is_booked"],
        "args": [[], ["ghost", 0], ["ghost"], ["ghost"]],
        "tags": ["edge"],
    },
    {
        "id": "h04",
        "ops": ["SeatStore", "add", "version", "book", "version", "is_booked"],
        "args": [[], ["c3"], ["c3"], ["c3", 0], ["c3"], ["c3"]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["SeatStore", "add", "book", "book", "version", "book", "version"],
        "args": [[], ["d"], ["d", 0], ["d", 1], ["d"], ["d", 1], ["d"]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": [
            "SeatStore",
            "add",
            "add",
            "book",
            "add",
            "version",
            "book",
            "is_booked",
            "is_booked",
        ],
        "args": [[], ["x"], ["y"], ["x", 0], ["x"], ["x"], ["y", 0], ["x"], ["y"]],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": ["SeatStore", "add", "book", "book", "book", "version"],
        "args": [[], ["e"], ["e", -1], ["e", 1], ["e", 0], ["e"]],
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
    seats = ("a", "b", "c")
    kinds = ("add", "book", "version", "is_booked")
    out = []
    for i in range(n):
        ops, args = ["SeatStore"], [[]]
        for _ in range(12):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = kinds[(state >> 16) & 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            seat = seats[(state >> 16) - 3 * ((state >> 16) // 3)]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            ver = (state >> 16) & 3
            ops.append(kind)
            args.append([seat, ver] if kind == "book" else [seat])
        ops.append("version")
        args.append(["a"])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
