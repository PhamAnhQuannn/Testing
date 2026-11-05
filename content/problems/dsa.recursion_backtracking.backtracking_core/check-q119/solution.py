def subsets(nums):
    res = []
    cur = []

    def go(i):
        if i == len(nums):
            res.append(cur[:])
            return
        go(i + 1)
        cur.append(nums[i])
        go(i + 1)
        cur.pop()

    go(0)
    return sorted(res, key=lambda x: (len(x), x))
