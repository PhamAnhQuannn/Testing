def search_range(nums, target):
    import bisect

    i = bisect.bisect_left(nums, target)
    if i == len(nums) or nums[i] != target:
        return [-1, -1]
    return [i, bisect.bisect_right(nums, target) - 1]
