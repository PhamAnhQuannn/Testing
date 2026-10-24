def get_concatenation(nums):
    # Lỗi: mỗi phần tử được lặp ngay cạnh nó, thay vì lặp cả list.
    return [x for x in nums for _ in range(2)]
