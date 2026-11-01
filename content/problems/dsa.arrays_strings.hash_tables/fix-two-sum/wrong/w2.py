def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [i, seen[need]]
        seen[x] = i
    return []
