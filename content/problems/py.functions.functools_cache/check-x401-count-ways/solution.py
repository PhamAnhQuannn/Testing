from functools import cache


def count_ways(coins, amount):
    @cache
    def go(i, rem):
        if rem == 0:
            return 1
        if rem < 0 or i == len(coins):
            return 0
        return go(i, rem - coins[i]) + go(i + 1, rem)

    return go(0, amount)
