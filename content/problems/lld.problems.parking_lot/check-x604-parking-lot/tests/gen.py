"""Inputs of check-x604-parking-lot.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["ParkingLot", "park", "leave", "available"],
    "args": [[1, 1], ["car"], [1, 3], ["car"]],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["ParkingLot", "park", "park", "available", "park"],
        "args": [[1, 1], ["car"], ["car"], ["car"], ["moto"]],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["ParkingLot", "leave", "park", "leave", "leave"],
        "args": [[1, 1], [5, 2], ["moto"], [1, 2], [1, 2]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["ParkingLot", "park", "park", "leave", "leave", "available", "available"],
        "args": [[2, 2], ["car"], ["moto"], [1, 4], [2, 4], ["car"], ["moto"]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["ParkingLot", "park", "leave", "park", "leave", "available"],
        "args": [[1, 0], ["car"], [1, 0], ["car"], [2, 7], ["car"]],
        "tags": ["edge"],
    },
    {
        "id": "h05",
        "ops": ["ParkingLot", "park", "park", "park", "available", "leave", "available", "park"],
        "args": [[0, 2], ["car"], ["moto"], ["moto"], ["moto"], [2, 1], ["moto"], ["moto"]],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": ["ParkingLot", "available", "available", "park", "leave"],
        "args": [[3, 4], ["car"], ["moto"], ["moto"], [1, 10]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["ParkingLot", "park", "park", "leave", "park", "leave", "leave", "available"],
        "args": [[1, 1], ["moto"], ["moto"], [1, 2], ["moto"], [2, 3], [1, 1], ["moto"]],
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
    kinds = ("car", "moto")
    out = []
    for i in range(n):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        cars = (state >> 16) % 3
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        motos = (state >> 16) % 3
        ops, args = ["ParkingLot"], [[cars, motos]]
        for _ in range(10):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("park", "leave", "available")[(state >> 16) % 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            kind = kinds[(state >> 16) % 2]
            ops.append(op)
            if op == "leave":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                tid = 1 + (state >> 16) % 4
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([tid, (state >> 16) % 6])
            else:
                args.append([kind])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
