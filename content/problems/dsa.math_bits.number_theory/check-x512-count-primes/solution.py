def count_primes(n):
    if n < 3:
        return 0
    is_p = bytearray([1]) * n
    is_p[0] = is_p[1] = 0
    i = 2
    while i * i < n:
        if is_p[i]:
            for j in range(i * i, n, i):
                is_p[j] = 0
        i += 1
    return sum(is_p)
