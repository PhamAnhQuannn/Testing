"""Inputs of check-x701-bow; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["mèo", "ăn", "cá", "mèo"], ["mèo", "ăn", "cá", "chó"]]},
    {"id": "s2", "args": [[], ["a", "b"]]},
]

HIDDEN = [
    {"id": "h01", "args": [["a", "b", "a"], ["a", "b", "c"]], "tags": []},
    {"id": "h02", "args": [[], ["x"]], "tags": ["edge"]},
    {"id": "h03", "args": [["x", "x"], ["x", "x"]], "tags": ["edge"]},
    {"id": "h04", "args": [["a", "b"], []], "tags": ["edge"]},
    {"id": "h05", "args": [[], []], "tags": ["edge"]},
    {"id": "h06", "args": [["the", "cat", "the", "dog"], ["the", "cat", "bird"]], "tags": []},
    {"id": "h07", "args": [["a"], ["a"]], "tags": []},
    {"id": "h08", "args": [["a", "a", "a", "a", "a"], ["b", "a", "c"]], "tags": []},
    {"id": "h09", "args": [["mèo", "chó", "cá"], ["cá", "chó", "mèo", "cá"]], "tags": []},
    {"id": "h10", "args": [["x", "y", "z", "x", "y", "x"], ["x", "y", "z", "w"]], "tags": []},
]

_ALPHABET = ["a", "b", "c", "d", "e", "f", "mèo", "cá"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        m = (x >> 8) % 9
        x = (x * 1103515245 + 12345) % 2147483648
        k = (x >> 8) % 6
        doc = []
        for _j in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            doc.append(_ALPHABET[(x >> 8) % len(_ALPHABET)])
        vocab = []
        for _j in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            vocab.append(_ALPHABET[(x >> 8) % len(_ALPHABET)])
        out.append([doc, vocab])
    return out


for _i, _a in enumerate(_lcg(29, 6)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
