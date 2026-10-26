def smaller_numbers_than_current(nums: list[int]) -> list[int]:
    distinct = set(nums)
    return [len([y for y in distinct if y < x]) for x in nums]
