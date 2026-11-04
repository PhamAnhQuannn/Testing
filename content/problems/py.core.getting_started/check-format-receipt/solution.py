def format_receipt(items):
    def money(cents):
        return f"{cents // 100}.{cents % 100:02d}"

    lines = []
    total = 0
    for it in items:
        name, qty, price = it.split(",")
        qty, price = int(qty), int(price)
        line_total = qty * price
        total += line_total
        lines.append(f"{name} x{qty} {money(line_total)}")
    lines.append("TOTAL " + money(total))
    return "\n".join(lines)
