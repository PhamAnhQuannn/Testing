def permutations(nums):
    res = []
    used = [False] * len(nums)
    cur = []

    def go():
        if len(cur) == len(nums):
            res.append(cur[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            cur.append(x)
            go()
            cur.pop()
            used[i] = False

    go()
    return sorted(res)
