def index_lookup(sorted_keys, targets):
    result = []
    for t in targets:
        lo = 0
        hi = len(sorted_keys) - 1
        pos = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            v = sorted_keys[mid]
            if v == t:
                pos = mid
                break
            if v < t:
                lo = mid + 1
            else:
                hi = mid - 1
        result.append(pos)
    return result
