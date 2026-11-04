from bisect import bisect_left, bisect_right


def bisect_ranges(sorted_xs, queries):
    return [[bisect_left(sorted_xs, q), bisect_right(sorted_xs, q)] for q in queries]
