"""Inputs of check-x841-cache-decision; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [{"age": "10"}, {"max-age": "60"}]},
    {"id": "s2", "args": [{"age": "100"}, {"max-age": "60"}]},
]

HIDDEN = [
    {"id": "h01", "args": [{}, {}], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [{}, {"no-store": "1"}], "tags": ["no-store"]},
    {"id": "h03", "args": [{"age": "5"}, {"no-cache": "1"}], "tags": ["no-cache"]},
    {"id": "h04", "args": [{"age": "10"}, {"max-age": "60"}], "tags": ["fresh"]},
    {"id": "h05", "args": [{"age": "100"}, {"max-age": "60"}], "tags": ["stale"]},
    {"id": "h06", "args": [{}, {"max-age": "60"}], "tags": ["no-age-header"]},
    {"id": "h07", "args": [{"age": "60"}, {"max-age": "60"}], "tags": ["boundary", "stale"]},
    {"id": "h08", "args": [{"age": "59"}, {"max-age": "60"}], "tags": ["boundary", "fresh"]},
    {
        "id": "h09",
        "args": [{"age": "1"}, {"no-store": "1", "max-age": "3600"}],
        "tags": ["no-store-beats-fresh"],
    },
    {
        "id": "h10",
        "args": [{"age": "1"}, {"no-store": "1", "no-cache": "1"}],
        "tags": ["no-store-beats-no-cache"],
    },
    {
        "id": "h11",
        "args": [{"age": "1"}, {"no-cache": "1", "max-age": "3600"}],
        "tags": ["no-cache-beats-fresh"],
    },
    {"id": "h12", "args": [{"age": "0"}, {"max-age": "0"}], "tags": ["boundary", "zero"]},
    {"id": "h13", "args": [{"age": "0"}, {"max-age": "1"}], "tags": ["boundary", "zero"]},
    {"id": "h14", "args": [{"age": "5"}, {}], "tags": ["no-max-age"]},
    {"id": "h15", "args": [{"host": "x.com"}, {"no-cache": ""}], "tags": ["empty-value"]},
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        req = {}
        resp = {}
        x = _next(x)
        if (x >> 8) % 6 == 0:
            resp["no-store"] = "1"
        x = _next(x)
        if (x >> 8) % 6 == 0:
            resp["no-cache"] = "1"
        x = _next(x)
        if (x >> 8) % 4 != 0:
            x = _next(x)
            resp["max-age"] = str((x >> 8) % 10)
        x = _next(x)
        if (x >> 8) % 4 != 0:
            x = _next(x)
            req["age"] = str((x >> 8) % 10)
        out.append([req, resp])
    return out


for _i, _a in enumerate(_lcg(41, 12)):
    HIDDEN.append({"id": f"h{16 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
