import math


def zscore_anomalies(series, threshold):
    n = len(series)
    if n == 0:
        return []
    mean = sum(series) / n
    var = sum((x - mean) ** 2 for x in series) / n
    std = math.sqrt(var)
    if std == 0:
        return []
    return [i for i, x in enumerate(series) if abs(x - mean) / std > threshold]
