def largest_number(nums):
    from functools import cmp_to_key

    s = sorted(
        map(str, nums),
        key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1 if a + b < b + a else 0),
    )
    r = "".join(s)
    return "0" if r[0] == "0" else r
