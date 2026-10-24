def find_numbers(nums):
    # Lỗi: chỉ nhận số có đúng 2 chữ số, bỏ sót 4 và 6 chữ số.
    return sum(1 for x in nums if 10 <= x <= 99)
