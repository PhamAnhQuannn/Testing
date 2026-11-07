import re


def url_for(rules, endpoint, params):
    for name, pattern in rules:
        if name == endpoint:
            return re.sub(r"\{(\w+)\}", lambda m: str(params[m.group(1)]), pattern)
    return ""
