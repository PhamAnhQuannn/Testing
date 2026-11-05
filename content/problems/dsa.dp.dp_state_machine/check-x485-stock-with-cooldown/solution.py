def max_profit_cooldown(prices):
    hold, sold, rest = -(10**9), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
