import math


def conf_interval(p_hat, n):
    se = math.sqrt(p_hat * (1 - p_hat) / n)
    return [round(p_hat - 1.96 * se, 6), round(p_hat + 1.96 * se, 6)]
