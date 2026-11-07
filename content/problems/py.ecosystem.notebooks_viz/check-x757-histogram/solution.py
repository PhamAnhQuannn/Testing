def histogram(values, k):
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [len(values)] + [0] * (k - 1)
    width = (hi - lo) / k
    counts = [0] * k
    for v in values:
        i = min(int((v - lo) / width), k - 1)
        counts[i] += 1
    return counts
