def positive_column_sums(rows):
    width = max((len(r) for r in rows), default=0)
    return [sum(r[j] for r in rows if j < len(r) and r[j] > 0) for j in range(width)]
