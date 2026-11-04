def k_closest(arr, k, x):
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])
