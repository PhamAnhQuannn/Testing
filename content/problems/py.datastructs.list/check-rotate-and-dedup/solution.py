def rotate_and_dedup(xs, k):
    if not xs:
        return []
    n = len(xs)
    k %= n
    rot = xs[n - k :] + xs[: n - k]
    seen = set()
    out = []
    for v in rot:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out
