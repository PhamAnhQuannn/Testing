def duplicate_zeros(arr):
    n = len(arr)
    i = 0
    while i < n:
        if arr[i] == 0:
            for j in range(n - 1, i + 1, -1):  # dời từng phần tử sang phải: O(n) mỗi số 0
                arr[j] = arr[j - 1]
            if i + 1 < n:
                arr[i + 1] = 0
            i += 1
        i += 1
