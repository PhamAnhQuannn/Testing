def two_sum_sorted(nums, target):
    i, j = (0, len(nums) - 1)
    while i < j:
        s = nums[i] + nums[j]
        if s == target:
            return [i + 1, j + 1]
        if s < target:
            i += 1
        else:
            j -= 1
    return []
