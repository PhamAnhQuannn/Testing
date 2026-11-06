"""Inputs of check-x625-logger.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Logger", "add_handler", "add_handler", "log", "handler_count"],
    "args": [[], ["console", "DEBUG"], ["file", "ERROR"], ["INFO", "hi"], []],
}

HIDDEN = [
    {
        "id": "h01",
        "ops": ["Logger", "log", "handler_count"],
        "args": [[], ["ERROR", "x"], []],
        "tags": ["edge"],
    },
    {
        "id": "h02",
        "ops": ["Logger", "add_handler", "add_handler", "log", "log"],
        "args": [[], ["a", "DEBUG"], ["b", "DEBUG"], ["DEBUG", "m"], ["ERROR", "m"]],
        "tags": [],
    },
    {
        "id": "h03",
        "ops": ["Logger", "add_handler", "add_handler", "log", "handler_count"],
        "args": [[], ["a", "ERROR"], ["b", "ERROR"], ["DEBUG", "m"], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["Logger", "add_handler", "add_handler", "add_handler", "log", "log"],
        "args": [
            [],
            ["x", "ERROR"],
            ["y", "DEBUG"],
            ["z", "INFO"],
            ["ERROR", "boom"],
            ["INFO", "i"],
        ],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["Logger", "add_handler", "add_handler", "log", "log", "log", "handler_count"],
        "args": [
            [],
            ["f", "INFO"],
            ["c", "INFO"],
            ["DEBUG", "d"],
            ["INFO", "i"],
            ["ERROR", "e"],
            [],
        ],
        "tags": [],
    },
    {
        "id": "h06",
        "ops": [
            "Logger",
            "add_handler",
            "add_handler",
            "log",
            "handler_count",
            "add_handler",
            "log",
        ],
        "args": [
            [],
            ["a", "INFO"],
            ["a", "INFO"],
            ["INFO", "m"],
            [],
            ["b", "DEBUG"],
            ["INFO", "m"],
        ],
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
    levels = ("DEBUG", "INFO", "ERROR")
    out = []
    for i in range(n):
        ops, args = ["Logger"], [[]]
        for j in range(10):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            op = ("add_handler", "log", "handler_count")[(state >> 16) % 3]
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            lvl = levels[(state >> 16) % 3]
            ops.append(op)
            if op == "add_handler":
                args.append([f"h{j}", lvl])
            elif op == "log":
                args.append([lvl, f"m{j}"])
            else:
                args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
