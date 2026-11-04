import re


def mask_digits(s):
    return re.sub(r"\d{4,}", lambda m: "*" * len(m.group()), s)
