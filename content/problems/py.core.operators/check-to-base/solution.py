def to_base(n, b):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    out = []
    while n > 0:
        out.append(digits[n % b])
        n //= b
    return sign + "".join(reversed(out))
