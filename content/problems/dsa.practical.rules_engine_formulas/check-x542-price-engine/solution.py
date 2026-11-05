def price_after(price, rules):
    for rule in rules:
        kind, value = rule.split()
        amount = int(value)
        if kind == "percent":
            price -= price * amount // 100
        else:
            price -= amount
        if price < 0:
            price = 0
    return price
