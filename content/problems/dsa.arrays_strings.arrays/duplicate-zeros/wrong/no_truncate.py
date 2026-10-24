def duplicate_zeros(arr):
    # Lỗi: list dài thêm thay vì giữ độ dài ban đầu.
    i = 0
    while i < len(arr):
        if arr[i] == 0:
            arr.insert(i, 0)
            i += 1
        i += 1
