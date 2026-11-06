import math


def sample_size(p, mde):
    return math.ceil(16 * p * (1 - p) / (mde * mde))
