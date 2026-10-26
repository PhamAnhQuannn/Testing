def rotate(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    k %= n
    return nums[n - k :] + nums[: n - k]
