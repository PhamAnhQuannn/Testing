def majority_element(nums: list[int]) -> int:
    for x in nums:
        if nums.count(x) > len(nums) // 2:
            return x
    return nums[0]
