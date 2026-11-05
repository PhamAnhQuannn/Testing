"""Inputs of check-x613-seat-booking.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["BookingSystem", "add_seat", "book", "book", "is_booked", "free_count"],
    "args": [[], ["a1"], ["a1"], ["a1"], ["a1"], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["BookingSystem", "add_seat", "book", "book", "is_booked", "free_count"],
        "args": [[], ["a1"], ["a1"], ["a1"], ["a1"], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["BookingSystem", "book", "is_booked", "cancel", "free_count"],
        "args": [[], ["ghost"], ["ghost"], ["ghost"], []],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["BookingSystem", "add_seat", "book", "cancel", "book", "is_booked", "free_count"],
        "args": [[], ["b2"], ["b2"], ["b2"], ["b2"], ["b2"], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["BookingSystem", "add_seat", "cancel", "is_booked", "cancel"],
        "args": [[], ["c3"], ["c3"], ["c3"], ["c3"]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": [
            "BookingSystem",
            "add_seat",
            "add_seat",
            "add_seat",
            "free_count",
            "book",
            "free_count",
            "book",
            "free_count",
            "cancel",
            "free_count",
        ],
        "args": [[], ["a"], ["b"], ["c"], [], ["a"], [], ["b"], [], ["a"], []],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["BookingSystem", "add_seat", "book", "add_seat", "is_booked", "free_count"],
        "args": [[], ["d"], ["d"], ["d"], ["d"], []],
        "tags": ["edge"],
    },
    {
        "id": "h07",
        "ops": ["BookingSystem", "free_count", "add_seat", "free_count"],
        "args": [[], [], ["z"], []],
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
    kinds = ("add_seat", "book", "cancel", "is_booked", "free_count")
    out = []
    for i in range(n):
        ops, args = ["BookingSystem"], [[]]
        for _ in range(12):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = kinds[(state >> 16) % 5]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            seat = seats[(state >> 16) % 3]
            ops.append(kind)
            args.append([] if kind == "free_count" else [seat])
        ops.append("free_count")
        args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
