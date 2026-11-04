def range_sum(nums, queries):
    n = len(nums)
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] += nums[i - 1]
        j = i + (i & -i)
        if j <= n:
            tree[j] += tree[i]

    def prefix(i):
        # sum of nums[0..i-1]
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    return [prefix(r + 1) - prefix(l) for l, r in queries]
