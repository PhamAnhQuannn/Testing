def estimate_rows(n, sels):
    result = n
    for num, den in sels:
        result = result * num // den
    return result
