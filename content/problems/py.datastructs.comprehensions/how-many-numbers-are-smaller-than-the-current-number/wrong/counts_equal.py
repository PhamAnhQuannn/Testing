def smaller_numbers_than_current(nums: list[int]) -> list[int]:
    return [len([y for y in nums if y <= x]) - 1 for x in nums]
