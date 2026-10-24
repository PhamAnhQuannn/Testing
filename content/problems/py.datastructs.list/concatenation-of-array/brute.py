def get_concatenation(nums):
    n = len(nums)
    return [nums[i % n] for i in range(2 * n)]
