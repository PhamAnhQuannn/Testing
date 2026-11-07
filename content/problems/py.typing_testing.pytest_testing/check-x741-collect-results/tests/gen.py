"""Inputs of check-x741-collect-results; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["t_add", 3, 3], ["t_sub", 1, 2], ["t_mul", 6, 6]]]},
    {"id": "s2", "args": [[]]},
]

HIDDEN = [
    {"id": "h01", "args": [[["a", 1, 1], ["b", 2, 2], ["c", "x", "x"]]], "tags": ["edge"]},
    {"id": "h02", "args": [[["a", 1, 2], ["b", 2, 3], ["c", "x", "y"]]], "tags": ["edge"]},
    {"id": "h03", "args": [[["cat", "12", 12], ["cat", "ab", "ab"]]], "tags": ["edge"]},
    {"id": "h04", "args": [[["dup", 1, 2], ["dup", 3, 4], ["dup", 5, 5]]], "tags": ["edge"]},
    {"id": "h05", "args": [[["only", 0, 0]]], "tags": ["edge"]},
    {"id": "h06", "args": [[["l1", [1, 2], [1, 2]], ["l2", [1, 2], [2, 1]]]], "tags": []},
    {"id": "h07", "args": [[["d1", {"a": 1}, {"a": 1}], ["d2", {"a": 1}, {"a": 2}]]], "tags": []},
    {"id": "h08", "args": [[["n", None, None], ["s", "", ""], ["z", 0, ""]]], "tags": []},
    {"id": "h09", "args": [[["f1", 1.5, 1.5], ["f2", 2, 2.0], ["f3", 3, 4]]], "tags": []},
    {"id": "h10", "args": [[["b", "True", True], ["e", [], []], ["x", "", []]]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = (x >> 8) % 9
        tests = []
        for _i in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            got = (x >> 8) % 5
            x = (x * 1103515245 + 12345) % 2147483648
            mode = (x >> 8) % 4
            if mode == 0:
                want = got
            elif mode == 1:
                want = (got + 1) % 5
            elif mode == 2:
                want = str(got)
            else:
                want = got
            x = (x * 1103515245 + 12345) % 2147483648
            name = "t" + str((x >> 8) % 4)
            tests.append([name, got, want])
        out.append([tests])
    return out


for _i, _a in enumerate(_lcg(41, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
