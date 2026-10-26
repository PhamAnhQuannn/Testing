def rotate(nums: list[int], k: int) -> list[int]:
    return nums[-k:] + nums[:-k]
