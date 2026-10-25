def is_pow3(n):
    if n < 1:
        return False
    if n == 1:
        return True
    return n % 3 == 0 and is_pow3(n // 3)
