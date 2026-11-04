def validate_age(values):
    def check(v):
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ValueError("invalid age")
        return v

    result = []
    for v in values:
        try:
            result.append(check(v))
        except ValueError:
            result.append("invalid")
    return result
