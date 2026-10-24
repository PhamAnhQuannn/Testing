def find_numbers(nums):
    # Lỗi: đếm số có số chữ số LẺ.
    return sum(1 for x in nums if len(str(x)) % 2 == 1)
