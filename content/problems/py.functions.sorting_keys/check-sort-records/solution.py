def sort_records(records, keys):
    index = {"name": 0, "dept": 1, "age": 2, "score": 3}
    out = list(records)
    for key in reversed(keys):
        desc = key.startswith("-")
        field = index[key.lstrip("-")]
        out.sort(key=lambda r, f=field: r[f], reverse=desc)
    return out
