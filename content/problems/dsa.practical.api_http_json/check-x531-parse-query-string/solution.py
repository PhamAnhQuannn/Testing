def parse_query_string(qs):
    result = {}
    for part in qs.split("&"):
        if not part:
            continue
        key, _, value = part.partition("=")
        result[key] = value
    return result
