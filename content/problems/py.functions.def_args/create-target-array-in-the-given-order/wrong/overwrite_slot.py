def create_target_array(nums: list[int], index: list[int]) -> list[int]:
    target = [0] * len(nums)
    for i in range(len(nums)):
        target[index[i]] = nums[i]
    return target
