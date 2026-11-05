RULES = {"weekday": 10, "weekend": 15, "holiday": 20}


def fee(hours, rule):
    rate = RULES.get(rule, RULES["weekday"])
    return hours * rate
