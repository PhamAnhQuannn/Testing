def rank_students(records: list[list]) -> list[str]:
    pool = [(name, score) for name, score in records]
    order = []
    while pool:
        best = pool[0]
        for cand in pool[1:]:
            if cand[1] > best[1] or (cand[1] == best[1] and cand[0] < best[0]):
                best = cand
        order.append(best[0])
        pool.remove(best)
    return order
