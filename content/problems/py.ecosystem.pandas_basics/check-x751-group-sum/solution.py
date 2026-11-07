def group_sum(rows):
    total = {}
    for key, value in rows:
        total[key] = total.get(key, 0) + value
    return [[key, total[key]] for key in sorted(total)]
