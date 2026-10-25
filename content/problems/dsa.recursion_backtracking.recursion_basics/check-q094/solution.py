def kth_symbol(n, k):
    if n == 1:
        return 0
    p = kth_symbol(n - 1, (k + 1) // 2)
    return p if k % 2 == 1 else 1 - p
