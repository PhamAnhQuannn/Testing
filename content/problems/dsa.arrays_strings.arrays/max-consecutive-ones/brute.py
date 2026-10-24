def find_max_consecutive_ones(nums):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if all(x == 1 for x in nums[i : j + 1]):
                best = max(best, j - i + 1)
    return best
