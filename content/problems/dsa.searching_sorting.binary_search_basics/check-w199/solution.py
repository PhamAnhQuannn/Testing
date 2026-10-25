def first_bad(n, is_bad):
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad[mid - 1]:
            hi = mid
        else:
            lo = mid + 1
    return lo
