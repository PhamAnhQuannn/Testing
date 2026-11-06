def kfold_indices(n, k):
    q, r = divmod(n, k)
    folds = []
    start = 0
    for i in range(k):
        size = q + 1 if i < r else q
        folds.append(list(range(start, start + size)))
        start += size
    return folds
