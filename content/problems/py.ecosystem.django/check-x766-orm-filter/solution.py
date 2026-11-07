def orm_filter(rows, conds, order_by):
    kept = [r for r in rows if all(r[k] == v for k, v in conds.items())]
    return sorted(kept, key=lambda r: [r[k] for k in order_by])
