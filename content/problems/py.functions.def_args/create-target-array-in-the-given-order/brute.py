def create_target_array(nums: list[int], index: list[int]) -> list[int]:
    target = []
    for value, pos in zip(nums, index, strict=True):
        target = target[:pos] + [value] + target[pos:]
    return target
