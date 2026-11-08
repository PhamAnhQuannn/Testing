def resolve(records, name):
    seen = set()
    cur = name
    while cur in records and cur not in seen:
        seen.add(cur)
        rtype, value = records[cur]
        if rtype == "A":
            return value
        cur = value
    return None
