def count_windows(nums, k, threshold):
    need = k * threshold
    s = sum(nums[:k])
    count = 1 if s >= need else 0
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        if s >= need:
            count += 1
    return count
