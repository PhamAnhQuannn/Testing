def running_kth_largest(nums: list[int], k: int) -> list[int]:
    result = []
    for i in range(len(nums)):
        seen = sorted(nums[: i + 1], reverse=True)
        result.append(seen[k - 1] if len(seen) >= k else -1)
    return result
