def max_coins(nums):
    a = [1] + list(nums) + [1]
    n = len(a)
    # dp[l][r] = so xu toi da khi no het bong trong khoang mo (l, r)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            best = 0
            for k in range(l + 1, r):
                # k la qua bong no CUOI CUNG trong (l, r)
                v = dp[l][k] + a[l] * a[k] * a[r] + dp[k][r]
                if v > best:
                    best = v
            dp[l][r] = best
    return dp[0][n - 1]
