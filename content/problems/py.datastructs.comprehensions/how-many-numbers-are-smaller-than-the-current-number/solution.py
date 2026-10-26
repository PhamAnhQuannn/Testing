def smaller_numbers_than_current(nums: list[int]) -> list[int]:
    return [len([y for y in nums if y < x]) for x in nums]
