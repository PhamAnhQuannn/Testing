def equal_01(nums):
    first = {0: -1}
    s = best = 0
    for i, x in enumerate(nums):
        s += 1 if x else -1
        if s in first:
            best = max(best, i - first[s])
        else:
            first[s] = i
    return best
