from datetime import datetime


def days_between(a, b):
    fmt = "%Y-%m-%d"
    return abs((datetime.strptime(b, fmt) - datetime.strptime(a, fmt)).days)
