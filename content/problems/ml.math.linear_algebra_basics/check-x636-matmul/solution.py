def matmul(A, B):
    if not A or not B:
        return []
    n = len(A[0])
    if any(len(row) != n for row in A) or len(B) != n:
        return []
    p = len(B[0])
    if any(len(row) != p for row in B):
        return []
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(len(A))]
