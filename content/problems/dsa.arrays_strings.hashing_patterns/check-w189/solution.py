def pair_count(nums, k):
    seen = {}
    res = 0
    for x in nums:
        res += seen.get(k - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return res
