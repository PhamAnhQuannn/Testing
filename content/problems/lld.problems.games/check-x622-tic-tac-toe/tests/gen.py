"""Inputs of check-x622-tic-tac-toe; `expected` comes from solution.py via gen_hidden."""


def _b(rows):
    return [list(r) for r in rows]


SAMPLES = [
    {"id": "s1", "args": [_b(["XXX", "OO.", "..."])]},
    {"id": "s2", "args": [_b(["XOX", "OXO", "OXO"])]},
]

HIDDEN = [
    {"id": "h01", "args": [_b(["...", "...", "..."])], "tags": ["edge"]},
    {"id": "h02", "args": [_b(["XOX", "XOO", "OXX"])], "tags": ["edge"]},
    {"id": "h03", "args": [_b(["...", "OOO", "X.X"])], "tags": ["row"]},
    {"id": "h04", "args": [_b(["XO.", "XO.", "X.."])], "tags": ["col"]},
    {"id": "h05", "args": [_b([".OX", ".XO", "XO."])], "tags": ["anti_diag"]},
    {"id": "h06", "args": [_b(["OX.", "XO.", "X.O"])], "tags": ["diag"]},
    {"id": "h07", "args": [_b(["XXO", "OOX", "XOX"])], "tags": ["draw"]},
    {"id": "h08", "args": [_b(["XO.", ".X.", "O.."])], "tags": ["none"]},
    {"id": "h09", "args": [_b(["XOX", "OXO", "..."])], "tags": ["none"]},
    {"id": "h10", "args": [_b([".OX", ".OX", "..X"])], "tags": ["col"]},
    {"id": "h11", "args": [_b(["XXO", "XOO", "OXX"])], "tags": ["anti_diag"]},
    {"id": "h12", "args": [_b(["OXX", "XOO", "XXO"])], "tags": ["diag"]},
]

_FIXED = [
    ["XXX", "OO.", "..."],
    ["OOO", "XX.", "X.."],
    ["X..", "OX.", "O.X"],
    ["XOX", "OXO", "OXO"],
    ["XOX", "XOO", "OXX"],
    ["...", ".X.", "..."],
    ["XO.", "OX.", "..O"],
    ["O.X", ".XO", "XO."],
]


def _lcg(seed, n):
    """Deterministic: pick a fixed board and optionally mirror/flip it."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        rows = list(_FIXED[(x >> 8) % len(_FIXED)])
        x = (x * 1103515245 + 12345) % 2147483648
        if (x >> 8) % 2 == 1:
            rows = [r[::-1] for r in rows]
        x = (x * 1103515245 + 12345) % 2147483648
        if (x >> 8) % 2 == 1:
            rows = rows[::-1]
        out.append([_b(rows)])
    return out


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
