def rotate(nums: list[int], k: int) -> list[int]:
    result = list(nums)
    for _ in range(k):
        last = result.pop()
        result.insert(0, last)
    return result
