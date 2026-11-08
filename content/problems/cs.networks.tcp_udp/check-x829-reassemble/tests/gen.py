"""Inputs of check-x829-reassemble; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[5, "world"], [0, "hello"]]]},
    {"id": "s2", "args": [[[0, "ab"], [2, "cd"], [2, "cd"], [6, "zz"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[[0, "a"]]], "tags": ["edge", "single"]},
    {"id": "h03", "args": [[[3, "abc"]]], "tags": ["edge", "gap-at-start"]},
    {
        "id": "h04",
        "args": [[[4, "ef"], [0, "ab"], [2, "cd"]]],
        "tags": ["out-of-order"],
    },
    {
        "id": "h05",
        "args": [[[0, "ab"], [0, "ab"], [2, "c"]]],
        "tags": ["duplicate-seq"],
    },
    {
        "id": "h06",
        "args": [[[0, "abc"], [5, "xyz"], [3, "de"]]],
        "tags": ["gap-stops", "out-of-order"],
    },
    {
        "id": "h07",
        "args": [[[0, "ab"], [2, "cd"], [4, "ef"], [6, "gh"]]],
        "tags": ["contiguous-chain"],
    },
    {
        "id": "h08",
        "args": [[[0, "hello"], [2, "llo"], [5, "world"]]],
        "tags": ["overlap-skipped"],
    },
    {
        "id": "h09",
        "args": [[[0, "abc"], [1, "bcd"], [3, "d"]]],
        "tags": ["overlap-skipped"],
    },
    {
        "id": "h10",
        "args": [[[0, "aa"], [0, "bb"], [2, "c"]]],
        "tags": ["equal-seq-stable"],
    },
    {
        "id": "h11",
        "args": [[[1, "bc"], [3, "d"]]],
        "tags": ["edge", "gap-at-start"],
    },
    {
        "id": "h12",
        "args": [[[2, "c"], [1, "b"], [0, "a"], [3, "d"], [2, "c"]]],
        "tags": ["reverse-order", "duplicate-seq"],
    },
]

ALPHABET = "abcde"


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        # contiguous construction: chunks of length 1..3 covering a stream
        x = _next(x)
        count = (x >> 8) % 7
        segs = []
        offset = 0
        for _r in range(count):
            x = _next(x)
            size = (x >> 8) % 3 + 1
            data = ""
            for _c in range(size):
                x = _next(x)
                data += ALPHABET[(x >> 8) % len(ALPHABET)]
            segs.append([offset, data])
            offset += size
        # optionally drop one chunk to create a gap
        x = _next(x)
        if segs and (x >> 8) % 3 == 0:
            x = _next(x)
            del segs[(x >> 8) % len(segs)]
        # optionally duplicate one chunk
        x = _next(x)
        if segs and (x >> 8) % 2 == 0:
            x = _next(x)
            segs.append(list(segs[(x >> 8) % len(segs)]))
        # shuffle (Fisher-Yates)
        for i in range(len(segs) - 1, 0, -1):
            x = _next(x)
            j = (x >> 8) % (i + 1)
            segs[i], segs[j] = segs[j], segs[i]
        out.append([segs])
    return out


for _i, _a in enumerate(_lcg(41, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
