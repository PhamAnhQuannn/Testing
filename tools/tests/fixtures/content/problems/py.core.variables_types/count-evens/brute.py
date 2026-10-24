def count_evens(nums):
    n = 0
    for x in nums:
        if x % 2 == 0:
            n += 1
    return n
