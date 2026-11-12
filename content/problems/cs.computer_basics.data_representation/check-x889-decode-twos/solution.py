def decode_twos(bits):
    if not bits:
        return 0
    n = len(bits)
    value = 0
    for i, b in enumerate(bits):
        weight = 1 << (n - 1 - i)
        if i == 0:
            value -= b * weight
        else:
            value += b * weight
    return value
