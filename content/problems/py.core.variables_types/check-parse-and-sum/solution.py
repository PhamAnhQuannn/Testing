import contextlib


def parse_and_sum(tokens):
    total = 0
    for tok in tokens:
        t = tok.strip()
        low = t.lower()
        if low == "true":
            total += 1
            continue
        if low == "false":
            continue
        try:
            total += int(t)
        except ValueError:
            with contextlib.suppress(ValueError):
                total += float(t)
    return f"{total:.2f}"
