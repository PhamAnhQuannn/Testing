def live_objects(refs, roots):
    graph = {int(k): v for k, v in refs.items()}
    seen = set()
    stack = [int(r) for r in roots]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for m in graph.get(n, []):
            stack.append(int(m))
    return sorted(seen)
