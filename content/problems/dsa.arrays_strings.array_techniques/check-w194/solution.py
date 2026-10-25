def dedupe_sorted(nums):
    w = 0
    for x in nums:
        if w == 0 or x != nums[w - 1]:
            nums[w] = x
            w += 1
    return w
