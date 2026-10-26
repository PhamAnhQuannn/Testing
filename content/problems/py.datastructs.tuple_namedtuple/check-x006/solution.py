def best_scorer(records):
    best_name, best_score = records[0]
    for name, score in records:
        if score > best_score:
            best_name, best_score = name, score
    return best_name, best_score
