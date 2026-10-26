def num_identical_pairs(nums: list[int]) -> int:
    seen: dict[int, int] = {}
    total = 0
    for x in nums:
        total += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return total
