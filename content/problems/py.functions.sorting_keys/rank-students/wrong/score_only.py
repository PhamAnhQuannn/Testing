def rank_students(records: list[list]) -> list[str]:
    ranked = sorted(records, key=lambda r: r[1], reverse=True)
    return [r[0] for r in ranked]
