def duplicate_zeros(arr):
    # Lỗi: đi từ trái sang phải và ghi đè lên phần tử chưa kịp đọc.
    for i in range(len(arr) - 1):
        if arr[i] == 0:
            arr[i + 1] = 0
