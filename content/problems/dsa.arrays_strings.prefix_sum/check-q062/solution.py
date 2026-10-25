def count_zero_sum(nums):
    seen = {0: 1}
    s = 0
    res = 0
    for x in nums:
        s += x
        res += seen.get(s, 0)
        seen[s] = seen.get(s, 0) + 1
    return res
