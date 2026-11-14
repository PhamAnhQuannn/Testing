import numpy as np


def std_dev(xs):
    return round(float(np.std(np.array(xs, dtype=float))), 6)
