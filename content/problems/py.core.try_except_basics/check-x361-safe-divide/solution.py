def safe_divide(pairs):
    result = []
    for a, b in pairs:
        try:
            result.append(a // b)
        except ZeroDivisionError:
            result.append("error")
    return result
