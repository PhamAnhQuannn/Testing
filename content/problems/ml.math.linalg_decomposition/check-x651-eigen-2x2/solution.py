import math


def eigenvalues_2x2(A):
    a, b = A[0]
    c, d = A[1]
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    if disc < 0:
        return []
    r = math.sqrt(disc)
    return [round((tr - r) / 2, 6), round((tr + r) / 2, 6)]
