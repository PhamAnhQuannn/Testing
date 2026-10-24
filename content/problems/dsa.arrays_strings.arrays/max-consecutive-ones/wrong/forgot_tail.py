def find_max_consecutive_ones(nums):
    # Lỗi: chỉ cập nhật kỉ lục khi gặp số 0, nên đoạn nằm ở cuối list bị bỏ sót.
    best = run = 0
    for x in nums:
        if x == 1:
            run += 1
        else:
            best = max(best, run)
            run = 0
    return best
