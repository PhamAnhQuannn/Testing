def fd_violations(rows, det, dep):
    groups = {}
    for row in rows:
        groups.setdefault(row[det], set()).add(row[dep])
    return sorted(k for k, vals in groups.items() if len(vals) > 1)
