def majority(nums):
    cand, cnt = (None, 0)
    for x in nums:
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
    return cand
