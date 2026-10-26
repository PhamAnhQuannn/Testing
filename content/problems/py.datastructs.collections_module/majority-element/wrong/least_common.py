from collections import Counter


def majority_element(nums: list[int]) -> int:
    return Counter(nums).most_common()[-1][0]
