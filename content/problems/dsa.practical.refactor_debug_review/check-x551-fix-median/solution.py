def median(nums):
    s = sorted(nums)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    v = (s[n // 2 - 1] + s[n // 2]) / 2
    return int(v) if v == int(v) else v
