"""Inputs of check-x838-verify-chain; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["leaf", "int"], ["int", "root"], ["root", "root"]]]},
    {"id": "s2", "args": [[["leaf", "int"], ["x", "root"], ["root", "root"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[["root", "root"]]], "tags": ["edge", "single-root"]},
    {"id": "h03", "args": [[["leaf", "leaf2"]]], "tags": ["edge", "single-not-self-signed"]},
    {
        "id": "h04",
        "args": [[["leaf", "int"], ["int", "root"], ["root", "root"]]],
        "tags": ["valid-3"],
    },
    {
        "id": "h05",
        "args": [[["leaf", "root"], ["root", "root"]]],
        "tags": ["valid-2"],
    },
    {
        "id": "h06",
        "args": [[["leaf", "int"], ["int", "root"]]],
        "tags": ["root-not-self-signed"],
    },
    {
        "id": "h07",
        "args": [[["leaf", "int"], ["x", "root"], ["root", "root"]]],
        "tags": ["broken-middle"],
    },
    {
        "id": "h08",
        "args": [[["leaf", "other"], ["int", "root"], ["root", "root"]]],
        "tags": ["broken-leaf"],
    },
    {
        "id": "h09",
        "args": [[["leaf", "i1"], ["i1", "i2"], ["i2", "i3"], ["i3", "root"], ["root", "root"]]],
        "tags": ["valid-long"],
    },
    {
        "id": "h10",
        "args": [[["leaf", "i1"], ["i1", "i2"], ["i2", "i3"], ["i3", "root"]]],
        "tags": ["long-root-not-self-signed"],
    },
    {
        "id": "h11",
        "args": [[["root", "root"], ["leaf", "root"]]],
        "tags": ["reversed"],
    },
    {
        "id": "h12",
        "args": [[["leaf", "int"], ["int", "root"], ["root", "root"], ["root", "root"]]],
        "tags": ["valid-duplicate-root"],
    },
    {
        "id": "h13",
        "args": [[["a", "b"], ["b", "a"], ["a", "a"]]],
        "tags": ["cycle-like"],
    },
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        depth = (x >> 8) % 5  # number of non-root certs: 0..4
        names = []
        for k in range(depth + 1):
            x = _next(x)
            names.append(f"n{k}_{(x >> 8) % 100}")
        # names[0] leaf ... names[-1] root
        certs = [[names[k], names[k + 1]] for k in range(depth)]
        certs.append([names[-1], names[-1]])
        # optionally corrupt
        x = _next(x)
        mode = (x >> 8) % 4
        if mode == 1 and certs:
            # break a link
            x = _next(x)
            idx = (x >> 8) % len(certs)
            certs[idx][1] = certs[idx][1] + "_bad"
        elif mode == 2:
            # root no longer self-signed
            certs[-1][1] = "other_root"
        elif mode == 3 and len(certs) > 1:
            certs = certs[:-1]
        out.append([certs])
    return out


for _i, _a in enumerate(_lcg(83, 10)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
