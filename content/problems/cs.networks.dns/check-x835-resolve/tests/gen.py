"""Inputs of check-x835-resolve; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [{"www": ["CNAME", "web"], "web": ["A", "1.2.3.4"]}, "www"],
    },
    {
        "id": "s2",
        "args": [{"a": ["CNAME", "b"], "b": ["CNAME", "a"]}, "a"],
    },
]

HIDDEN = [
    {"id": "h01", "args": [{}, "x"], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [{"a": ["A", "1.1.1.1"]}, "b"], "tags": ["edge", "missing-name"]},
    {"id": "h03", "args": [{"a": ["A", "1.1.1.1"]}, "a"], "tags": ["direct-a"]},
    {
        "id": "h04",
        "args": [{"www": ["CNAME", "web"], "web": ["A", "1.2.3.4"]}, "www"],
        "tags": ["one-hop"],
    },
    {
        "id": "h05",
        "args": [
            {
                "a": ["CNAME", "b"],
                "b": ["CNAME", "c"],
                "c": ["CNAME", "d"],
                "d": ["A", "8.8.8.8"],
            },
            "a",
        ],
        "tags": ["multi-hop"],
    },
    {"id": "h06", "args": [{"a": ["CNAME", "b"]}, "a"], "tags": ["cname-to-missing"]},
    {
        "id": "h07",
        "args": [{"a": ["CNAME", "b"], "b": ["CNAME", "a"]}, "a"],
        "tags": ["loop-2"],
    },
    {"id": "h08", "args": [{"a": ["CNAME", "a"]}, "a"], "tags": ["self-loop"]},
    {
        "id": "h09",
        "args": [
            {"a": ["CNAME", "b"], "b": ["CNAME", "c"], "c": ["CNAME", "a"]},
            "b",
        ],
        "tags": ["loop-3"],
    },
    {
        "id": "h10",
        "args": [
            {
                "x": ["CNAME", "y"],
                "y": ["CNAME", "z"],
                "z": ["CNAME", "y"],
                "w": ["A", "2.2.2.2"],
            },
            "x",
        ],
        "tags": ["loop-not-at-start"],
    },
    {
        "id": "h11",
        "args": [
            {
                "n0": ["CNAME", "n1"],
                "n1": ["CNAME", "n2"],
                "n2": ["CNAME", "n3"],
                "n3": ["CNAME", "n4"],
                "n4": ["CNAME", "n5"],
                "n5": ["CNAME", "n6"],
                "n6": ["CNAME", "n7"],
                "n7": ["A", "10.0.0.7"],
            },
            "n0",
        ],
        "tags": ["long-chain"],
    },
    {
        "id": "h12",
        "args": [
            {"a": ["CNAME", "b"], "b": ["A", "3.3.3.3"], "c": ["A", "4.4.4.4"]},
            "c",
        ],
        "tags": ["unrelated-records"],
    },
    {
        "id": "h13",
        "args": [{"a": ["CNAME", "b"], "b": ["A", "3.3.3.3"]}, "b"],
        "tags": ["start-at-a"],
    },
]

NAMES = ["n0", "n1", "n2", "n3", "n4", "n5"]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        count = (x >> 8) % 6 + 1
        records = {}
        for idx in range(count):
            nm = NAMES[idx]
            x = _next(x)
            if (x >> 8) % 3 == 0:
                x = _next(x)
                records[nm] = ["A", f"10.0.{idx}.{(x >> 8) % 256}"]
            else:
                x = _next(x)
                # target may be any known name or a dangling one
                pool = NAMES[: count + 1]
                records[nm] = ["CNAME", pool[(x >> 8) % len(pool)]]
        x = _next(x)
        query_pool = NAMES[: count + 1] + ["zz"]
        query = query_pool[(x >> 8) % len(query_pool)]
        out.append([records, query])
    return out


for _i, _a in enumerate(_lcg(53, 10)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
