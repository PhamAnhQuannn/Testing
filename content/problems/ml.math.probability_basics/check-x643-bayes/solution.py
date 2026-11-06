def bayes(prior, tpr, fpr):
    denom = tpr * prior + fpr * (1 - prior)
    if denom == 0:
        return 0.0
    return float(round(tpr * prior / denom, 6))
