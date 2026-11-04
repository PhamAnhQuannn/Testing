from collections import Counter


def max_pair_count(nums):
    if len(nums) < 2:
        return 0
    c = Counter(zip(nums, nums[1:]))
    return max(c.values())
