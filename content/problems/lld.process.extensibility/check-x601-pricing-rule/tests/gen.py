"""Inputs of check-x601-pricing-rule; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [2, "weekend"]},
    {"id": "s2", "args": [3, "weekday"]},
]

RULE_NAMES = ["weekday", "weekend", "holiday", "night", "vip"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        hours = (x >> 8) % 100
        x = (x * 1103515245 + 12345) % 2147483648
        rule = RULE_NAMES[(x >> 8) % len(RULE_NAMES)]
        out.append([hours, rule])
    return out


HIDDEN = [
    {"id": "h01", "args": [0, "weekday"], "tags": ["edge"]},
    {"id": "h02", "args": [0, "unknown"], "tags": ["edge"]},
    {"id": "h03", "args": [1, "weekday"], "tags": ["rule"]},
    {"id": "h04", "args": [4, "weekend"], "tags": ["rule"]},
    {"id": "h05", "args": [5, "holiday"], "tags": ["rule"]},
    {"id": "h06", "args": [7, "night"], "tags": ["unknown"]},
    {"id": "h07", "args": [3, ""], "tags": ["unknown"]},
    {"id": "h08", "args": [1000000, "holiday"], "tags": ["large"]},
]
for _i, _a in enumerate(_lcg(7, 12)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
