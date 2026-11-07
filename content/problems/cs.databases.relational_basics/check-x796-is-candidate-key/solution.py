def is_candidate_key(rows, cols):
    seen = set()
    for row in rows:
        key = tuple(row[c] for c in cols)
        if any(v is None for v in key):
            return False
        if key in seen:
            return False
        seen.add(key)
    return True
