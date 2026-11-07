"""Inputs of check-x744-parse-query; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["https://api.example.com/search?q=python&page=2"]},
    {"id": "s2", "args": ["https://x.io/a"]},
]

HIDDEN = [
    {"id": "h01", "args": ["https://x.io/a?"], "tags": ["edge"]},
    {"id": "h02", "args": ["https://x.io/a?k=1&k=2&k=3"], "tags": ["edge"]},
    {"id": "h03", "args": ["https://x.io/s?q=a%20b&n=1#frag"], "tags": ["edge"]},
    {"id": "h04", "args": ["https://x.io/a#only-fragment"], "tags": ["edge"]},
    {"id": "h05", "args": ["https://x.io/a?token=ab=cd"], "tags": ["edge"]},
    {"id": "h06", "args": ["https://x.io/a?x=1&y=2&z=3"], "tags": []},
    {"id": "h07", "args": ["http://localhost:8000/items?limit=10&offset=40"], "tags": []},
    {"id": "h08", "args": ["https://x.io/a?name=An%20Binh&city=Hue"], "tags": []},
    {"id": "h09", "args": ["https://x.io/p/q/r?a=1&b=2&a=3#end"], "tags": []},
    {"id": "h10", "args": ["/relative/path?id=7"], "tags": ["edge"]},
]

_HOSTS = ["https://api.example.com", "https://x.io", "http://localhost:8000"]
_PATHS = ["", "/a", "/search", "/v1/items"]
_KEYS = ["q", "page", "limit", "id", "tag"]
_VALS = ["python", "1", "20", "abc", "x%20y", "k9"]
_FRAGS = ["", "", "#top"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        host = _HOSTS[(x >> 8) % len(_HOSTS)]
        x = (x * 1103515245 + 12345) % 2147483648
        path = _PATHS[(x >> 8) % len(_PATHS)]
        x = (x * 1103515245 + 12345) % 2147483648
        n_params = (x >> 8) % 5
        pairs = []
        for _p in range(n_params):
            x = (x * 1103515245 + 12345) % 2147483648
            key = _KEYS[(x >> 8) % len(_KEYS)]
            x = (x * 1103515245 + 12345) % 2147483648
            val = _VALS[(x >> 8) % len(_VALS)]
            pairs.append(key + "=" + val)
        x = (x * 1103515245 + 12345) % 2147483648
        frag = _FRAGS[(x >> 8) % len(_FRAGS)]
        url = host + path
        if pairs:
            url = url + "?" + "&".join(pairs)
        out.append([url + frag])
    return out


for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
