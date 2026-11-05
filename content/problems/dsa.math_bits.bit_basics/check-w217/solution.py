def missing_number(nums):
    r = len(nums)
    for i, x in enumerate(nums):
        r ^= i ^ x
    return r


def is_pow2(n):
    return n > 0 and n & n - 1 == 0
