"""Inputs of check-x719-live-objects; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [{"1": [2], "2": [1], "3": []}, [1]]},
    {"id": "s2", "args": [{}, []]},
]

HIDDEN = [
    {"id": "h01", "args": [{"1": [2], "2": [3], "3": [1], "4": []}, [1]], "tags": ["edge"]},
    {"id": "h02", "args": [{"1": [2], "2": [], "3": [3]}, [1]], "tags": ["edge"]},
    {"id": "h03", "args": [{"1": [2], "2": [3], "3": []}, []], "tags": ["edge"]},
    {"id": "h04", "args": [{"1": [1]}, [1]], "tags": ["edge"]},
    {"id": "h05", "args": [{"1": [9], "2": []}, [1]], "tags": ["edge"]},
    {"id": "h06", "args": [{"1": [2], "2": [3], "3": [], "4": [5], "5": [4]}, [1, 4]], "tags": []},
    {"id": "h07", "args": [{"1": [2, 3], "2": [4], "3": [4], "4": [], "5": [1]}, [1]], "tags": []},
    {"id": "h08", "args": [{"1": [2], "2": [1], "3": [4], "4": [3]}, [3]], "tags": []},
    {"id": "h09", "args": [{}, [7, 3, 7]], "tags": ["edge"]},
    {
        "id": "h10",
        "args": [{"0": [1, 2], "1": [3], "2": [3], "3": [0], "4": [4]}, [2, 4]],
        "tags": [],
    },
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_ids = 1 + (x >> 8) % 8
        refs = {}
        for i in range(n_ids):
            x = (x * 1103515245 + 12345) % 2147483648
            deg = (x >> 8) % 3
            targets = []
            for _d in range(deg):
                x = (x * 1103515245 + 12345) % 2147483648
                targets.append((x >> 8) % (n_ids + 1))
            refs[str(i)] = targets
        x = (x * 1103515245 + 12345) % 2147483648
        n_roots = (x >> 8) % 3
        roots = []
        for _r in range(n_roots):
            x = (x * 1103515245 + 12345) % 2147483648
            roots.append((x >> 8) % n_ids)
        out.append([refs, roots])
    return out


for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
