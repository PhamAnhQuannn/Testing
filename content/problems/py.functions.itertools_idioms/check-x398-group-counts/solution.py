from itertools import groupby


def group_counts(words):
    ordered = sorted(words, key=len)
    return [[k, len(list(g))] for k, g in groupby(ordered, key=len)]
