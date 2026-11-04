from itertools import combinations


def pairs_with_sum(nums, target):
    pairs = (sorted(p) for p in combinations(nums, 2) if sum(p) == target)
    return sorted(pairs)
