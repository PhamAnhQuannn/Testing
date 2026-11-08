"""Inputs of check-x814-shard-of; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["a", "bb"], 3]},
    {"id": "s2", "args": [["user1", "user2", "order9"], 4]},
]

HIDDEN = [
    {"id": "h01", "args": [[], 3], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [["a", "bb", "ccc", "dddd"], 1], "tags": ["edge", "n1"]},
    {"id": "h03", "args": [["solo"], 5], "tags": ["edge", "single"]},
    {"id": "h04", "args": [[""], 7], "tags": ["edge", "empty-string"]},
    {"id": "h05", "args": [["", "a", ""], 2], "tags": ["edge", "empty-string"]},
    {"id": "h06", "args": [["k", "k", "k"], 4], "tags": ["repeated"]},
    {"id": "h07", "args": [["ab", "ba", "ab"], 5], "tags": ["repeated", "anagram"]},
    {
        "id": "h08",
        "args": [["abcdefghijklmnopqrstuvwxyz0123456789" * 3, "Z" * 100], 8],
        "tags": ["long"],
    },
    {"id": "h09", "args": [["a", "d", "g", "j"], 3], "tags": ["skew", "hot-shard"]},
    {"id": "h10", "args": [["x1", "y2", "z3", "w4", "v5"], 2], "tags": ["alnum"]},
    {"id": "h11", "args": [["id42", "id43", "id44", "id45", "id46"], 8], "tags": ["alnum"]},
    {"id": "h12", "args": [["a", "b", "c"], 100], "tags": ["large-n"]},
]

ALPHABET = "abcxyz019"


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        count = (x >> 8) % 8
        keys = []
        for _r in range(count):
            x = (x * 1103515245 + 12345) % 2147483648
            length = (x >> 8) % 7
            word = []
            for _c in range(length):
                x = (x * 1103515245 + 12345) % 2147483648
                word.append(ALPHABET[(x >> 8) % len(ALPHABET)])
            keys.append("".join(word))
        x = (x * 1103515245 + 12345) % 2147483648
        out.append([keys, (x >> 8) % 8 + 1])
    return out


for _i, _a in enumerate(_lcg(41, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
