def min_len(target, nums):
    l = s = 0
    best = float("inf")
    for r, x in enumerate(nums):
        s += x
        while s >= target:
            best = min(best, r - l + 1)
            s -= nums[l]
            l += 1
    return 0 if best == float("inf") else best
