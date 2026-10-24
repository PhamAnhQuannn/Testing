import time


def count_evens(nums):
    time.sleep(5)
    return sum(1 for x in nums if x % 2 == 0)
