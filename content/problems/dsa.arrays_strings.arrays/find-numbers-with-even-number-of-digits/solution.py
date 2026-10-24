def find_numbers(nums: list[int]) -> int:
    count = 0
    for x in nums:
        if len(str(x)) % 2 == 0:
            count += 1
    return count
