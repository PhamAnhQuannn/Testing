def range_sums(nums, queries):
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    return [p[r + 1] - p[l] for l, r in queries]
