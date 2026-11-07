"""Inputs of check-x736-map-reduce; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["a", "b", "a"], ["b", "c"]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[[], ["x"], ["x", "y"]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[], [], []]], "tags": ["edge"]},
    {"id": "h04", "args": [[["solo", "solo", "solo"]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["a"], ["a"], ["a"], ["a"]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["x", "y"], ["y", "z"], ["z", "x"]]], "tags": []},
    {"id": "h07", "args": [[["go", "run", "go"], [], ["run", "run", "jump"]]], "tags": []},
    {"id": "h08", "args": [[["Apple", "apple"], ["APPLE", "apple"]]], "tags": []},
    {"id": "h09", "args": [[["a", "b", "c", "d", "e"], ["e", "d", "c", "b", "a"]]], "tags": []},
    {"id": "h10", "args": [[["one"], ["two"], ["three"], ["one", "two", "three"]]], "tags": []},
]

_POOL = ["a", "b", "c", "d", "e", "foo", "bar", "baz", "x", "y"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_chunks = (x >> 8) % 6
        chunks = []
        for _c in range(n_chunks):
            x = (x * 1103515245 + 12345) % 2147483648
            n_words = (x >> 8) % 7
            words = []
            for _w in range(n_words):
                x = (x * 1103515245 + 12345) % 2147483648
                words.append(_POOL[(x >> 8) % len(_POOL)])
            chunks.append(words)
        out.append([chunks])
    return out


for _i, _a in enumerate(_lcg(17, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
