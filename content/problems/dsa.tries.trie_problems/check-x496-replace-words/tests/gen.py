"""Inputs of check-x496-replace-words; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["cat", "bat", "rat"], "the cattle was rattled"]},
    {"id": "s2", "args": [["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"]},
    {"id": "s3", "args": [["catt", "cat", "bat", "rat"], "the cattle was rattled by the battery"]},
]


def _lcg(seed):
    x = seed
    while True:
        x = (x * 1103515245 + 12345) % 2147483648
        yield x >> 8


def _word(g, lo, hi, alpha):
    n = lo + next(g) % (hi - lo + 1)
    return "".join(chr(97 + next(g) % alpha) for _ in range(n))


def _case(seed, nd, ns, alpha):
    g = _lcg(seed)
    dictionary = [_word(g, 1, 4, alpha) for _ in range(nd)]
    sentence = " ".join(_word(g, 1, 8, alpha) for _ in range(ns))
    return [dictionary, sentence]


HIDDEN = [
    {"id": "h01", "args": [[], "keep this sentence"], "tags": ["edge"]},
    {"id": "h02", "args": [["a"], "a"], "tags": ["edge"]},
    {"id": "h03", "args": [["abc"], "ab abc abcd x"], "tags": ["edge"]},
    {"id": "h04", "args": [["ab", "a", "abc"], "abcd abx a b"], "tags": ["edge"]},
    {"id": "h05", "args": [["zzz"], "word"], "tags": []},
    {"id": "h06", "args": _case(1, 5, 10, 3), "tags": []},
    {"id": "h07", "args": _case(2, 20, 30, 3), "tags": []},
    {"id": "h08", "args": _case(3, 50, 60, 4), "tags": []},
    {"id": "h09", "args": _case(4, 100, 100, 2), "tags": []},
    {"id": "h10", "args": _case(5, 300, 200, 5), "tags": []},
    {"id": "h11", "args": [["aaaaaaaaaa"], " ".join(["a" * 12] * 50)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
