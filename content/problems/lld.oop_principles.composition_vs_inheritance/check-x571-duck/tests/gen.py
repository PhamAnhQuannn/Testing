"""Inputs of check-x571-duck.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Duck", "perform_fly", "set_fly", "perform_fly", "perform_quack"],
    "args": [["fly", "quack"], [], ["noway"], [], []],
}

FLYS = ["fly", "noway"]
QUACKS = ["quack", "mute", "squeak"]


def _combo_rows():
    rows = []
    i = 0
    for f in FLYS:
        for q in QUACKS:
            i += 1
            rows.append(
                {
                    "id": f"h{i:02d}",
                    "ops": ["Duck", "perform_fly", "perform_quack"],
                    "args": [[f, q], [], []],
                    "tags": [],
                }
            )
    return rows


def hidden_inputs():
    rows = _combo_rows()
    rows += [
        {
            "id": "h07",
            "ops": ["Duck", "set_fly", "perform_fly", "set_fly", "perform_fly"],
            "args": [["fly", "squeak"], ["noway"], [], ["fly"], []],
            "tags": ["swap"],
        },
        {
            "id": "h08",
            "ops": ["Duck", "perform_fly", "perform_fly", "perform_quack", "perform_quack"],
            "args": [["noway", "mute"], [], [], [], []],
            "tags": ["edge", "repeat"],
        },
        {
            "id": "h09",
            "ops": ["Duck", "set_fly", "set_fly", "perform_fly", "perform_quack"],
            "args": [["noway", "quack"], ["noway"], ["fly"], [], []],
            "tags": ["swap"],
        },
    ]
    return rows


def small_inputs(seed, n):
    out = []
    state = seed % 2147483647 or 1
    for k in range(n):
        ops = ["Duck"]
        args = [[FLYS[0], QUACKS[0]]]
        state = (state * 48271) % 2147483647
        args[0] = [FLYS[state % 2], QUACKS[(state // 2) % 3]]
        for _ in range(6):
            state = (state * 48271) % 2147483647
            r = state % 3
            if r == 0:
                ops.append("perform_fly")
                args.append([])
            elif r == 1:
                ops.append("perform_quack")
                args.append([])
            else:
                ops.append("set_fly")
                args.append([FLYS[(state // 3) % 2]])
        out.append({"id": f"r{k}", "ops": ops, "args": args})
    return out


def sample_inputs():
    return [SAMPLE]
