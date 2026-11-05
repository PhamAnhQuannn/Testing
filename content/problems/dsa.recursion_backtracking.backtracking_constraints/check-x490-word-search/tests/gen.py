"""Inputs of check-x490-word-search; `expected` comes from solution.py via gen_hidden."""

BOARD = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]

SAMPLES = [
    {"id": "s1", "args": [BOARD, "ABCCED"]},
    {"id": "s2", "args": [BOARD, "SEE"]},
    {"id": "s3", "args": [BOARD, "ABCB"]},
]


def _board(seed, rows, cols, alphabet):
    """Seeded LCG board over `alphabet`."""
    x = seed
    out = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append(alphabet[(x >> 8) % len(alphabet)])
        out.append(row)
    return out


def _word(seed, length, alphabet):
    x = seed
    chars = []
    for _ in range(length):
        x = (x * 1103515245 + 12345) % 2147483648
        chars.append(alphabet[(x >> 8) % len(alphabet)])
    return "".join(chars)


HIDDEN = [
    {"id": "h01", "args": [[["a"]], "a"], "tags": ["edge"]},
    {"id": "h02", "args": [[["a"]], "b"], "tags": ["edge"]},
    {"id": "h03", "args": [[["a"]], "aa"], "tags": ["edge"]},
    {"id": "h04", "args": [[["a", "b"], ["c", "d"]], "abcdx"], "tags": ["edge"]},
    {"id": "h05", "args": [[["a", "b"], ["c", "d"]], "acdb"], "tags": []},
    {"id": "h06", "args": [[["a", "a"], ["a", "a"]], "aaaaa"], "tags": []},
    {"id": "h07", "args": [BOARD, "ABCESEEEFS"], "tags": []},
    {"id": "h08", "args": [_board(5, 5, 5, "ab"), "ababab"], "tags": []},
    {"id": "h09", "args": [_board(6, 6, 6, "abc"), _word(7, 8, "abc")], "tags": []},
    {"id": "h10", "args": [_board(8, 4, 6, "ab"), "aaaabbbb"], "tags": []},
    {"id": "h11", "args": [_board(9, 6, 6, "a"), "a" * 36], "tags": []},
    {"id": "h12", "args": [_board(10, 6, 6, "a"), "a" * 35 + "b"], "tags": []},
    {"id": "h13", "args": [[["a", "b", "c"]], "cba"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
