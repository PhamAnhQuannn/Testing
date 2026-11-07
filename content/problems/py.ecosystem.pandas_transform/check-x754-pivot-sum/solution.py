def pivot_sum(rows):
    result = {}
    for r, c, v in rows:
        inner = result.setdefault(r, {})
        inner[c] = inner.get(c, 0) + v
    return result
