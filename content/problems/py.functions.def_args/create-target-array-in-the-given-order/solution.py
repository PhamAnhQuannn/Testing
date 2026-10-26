def create_target_array(nums: list[int], index: list[int]) -> list[int]:
    target = []
    for i in range(len(nums)):
        target.insert(index[i], nums[i])
    return target
