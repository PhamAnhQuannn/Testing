def explained_variance_ratio(variances):
    total = sum(variances)
    if total == 0:
        return [0.0 for _ in variances]
    ratios = sorted((v / total for v in variances), reverse=True)
    return [round(r, 6) for r in ratios]
