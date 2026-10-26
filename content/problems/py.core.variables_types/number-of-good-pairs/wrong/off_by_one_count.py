def num_identical_pairs(nums: list[int]) -> int:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    return sum(c * (c + 1) // 2 for c in counts.values())
