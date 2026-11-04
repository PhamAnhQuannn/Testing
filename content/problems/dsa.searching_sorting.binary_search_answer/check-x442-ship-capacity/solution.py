def ship_capacity(weights, days):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        need, load = 1, 0
        for w in weights:
            if load + w > mid:
                need += 1
                load = 0
            load += w
        if need <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
