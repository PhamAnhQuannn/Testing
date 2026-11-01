def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        seen[x] = i
        need = target - x
        if need in seen:
            return [seen[need], i]
    return []
