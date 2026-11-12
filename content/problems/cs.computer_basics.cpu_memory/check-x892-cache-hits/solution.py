def cache_hits(accesses, num_lines):
    cache = {}
    hits = 0
    for addr in accesses:
        line = addr % num_lines
        if cache.get(line) == addr:
            hits += 1
        else:
            cache[line] = addr
    return hits
