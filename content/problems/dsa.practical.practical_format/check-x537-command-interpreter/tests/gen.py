"""Inputs of check-x537-command-interpreter; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["SET a 1", "SET b 2", "GET a", "GET b", "DEL a", "GET a"]]},
    {"id": "s2", "args": [["GET x"]]},
    {"id": "s3", "args": [["SET k v", "SET k w", "GET k"]]},
]


def _seeded(seed, n):
    """Deterministic command list of length n from a seeded LCG over a small key space."""
    x = seed
    keys = ["a", "b", "c", "d"]
    cmds = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        op = (x >> 8) % 3
        k = keys[(x >> 4) % len(keys)]
        if op == 0:
            cmds.append(f"SET {k} {(x >> 2) % 100}")
        elif op == 1:
            cmds.append(f"GET {k}")
        else:
            cmds.append(f"DEL {k}")
    return cmds


HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [["GET missing"]], "tags": ["edge"]},
    {"id": "h03", "args": [["SET x 5", "GET x", "DEL x", "GET x"]], "tags": ["edge"]},
    {"id": "h04", "args": [["DEL ghost", "GET ghost"]], "tags": ["edge"]},
    {"id": "h05", "args": [["SET a 1", "SET a 2", "SET a 3", "GET a"]], "tags": []},
    {"id": "h06", "args": [["SET a 1", "SET b 2", "GET a", "GET b", "GET a"]], "tags": []},
    {"id": "h07", "args": [_seeded(1, 20)], "tags": []},
    {"id": "h08", "args": [_seeded(2, 40)], "tags": []},
    {"id": "h09", "args": [_seeded(3, 60)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
