def climb(n, memo={}):
    if n <= 2:
        return n
    if n not in memo:
        memo[n] = climb(n - 1) + climb(n - 2)
    return memo[n]
