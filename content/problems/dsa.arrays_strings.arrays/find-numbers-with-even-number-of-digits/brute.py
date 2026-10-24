def find_numbers(nums):
    count = 0
    for x in nums:
        digits = 0
        while x > 0:
            x //= 10
            digits += 1
        if digits % 2 == 0:
            count += 1
    return count
