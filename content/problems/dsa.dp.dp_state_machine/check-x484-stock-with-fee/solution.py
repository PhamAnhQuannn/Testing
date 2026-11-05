def max_profit_fee(prices, fee):
    if not prices:
        return 0
    hold, cash = -prices[0], 0
    for p in prices[1:]:
        hold, cash = max(hold, cash - p), max(cash, hold + p - fee)
    return cash
