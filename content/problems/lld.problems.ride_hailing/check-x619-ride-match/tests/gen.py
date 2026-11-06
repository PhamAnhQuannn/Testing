"""Inputs of check-x619-ride-match.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["RideSystem", "add_driver", "add_driver", "request", "available_count"],
    "args": [[], [1, 10], [2, 5], [6], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["RideSystem", "request", "available_count"],
        "args": [[], [3], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["RideSystem", "add_driver", "add_driver", "request", "request"],
        "args": [[], [5, 0], [2, 10], [5], [5]],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["RideSystem", "add_driver", "add_driver", "add_driver", "request", "request"],
        "args": [[], [9, 4], [3, 6], [4, 5], [5], [5]],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["RideSystem", "add_driver", "request", "request", "complete", "request"],
        "args": [[], [1, 0], [0], [0], [1], [100]],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": [
            "RideSystem",
            "add_driver",
            "add_driver",
            "add_driver",
            "request",
            "request",
            "request",
            "request",
            "available_count",
        ],
        "args": [[], [1, -5], [2, 5], [3, 0], [1], [1], [1], [1], []],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": [
            "RideSystem",
            "add_driver",
            "add_driver",
            "request",
            "complete",
            "available_count",
            "request",
            "request",
        ],
        "args": [[], [4, 2], [8, 9], [3], [4], [], [3], [3]],
        "tags": [],
    },
    {
        "id": "h07",
        "ops": ["RideSystem", "add_driver", "complete", "available_count", "complete", "request"],
        "args": [[], [6, 1], [6], [], [99], [1]],
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
    out = []
    for i in range(n):
        ops, args = ["RideSystem"], [[]]
        for _ in range(12):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("add_driver", "request", "complete", "available_count")[(state >> 16) % 4]
            ops.append(op)
            if op == "add_driver":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                did = 1 + (state >> 16) % 4
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([did, (state >> 16) % 11 - 5])
            elif op == "request":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([(state >> 16) % 11 - 5])
            elif op == "complete":
                state = (state * 1103515245 + 12345) & 0x7FFFFFFF
                args.append([1 + (state >> 16) % 4])
            else:
                args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
