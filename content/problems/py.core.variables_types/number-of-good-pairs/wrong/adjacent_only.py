def num_identical_pairs(nums: list[int]) -> int:
    total = 0
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            total += 1
    return total
