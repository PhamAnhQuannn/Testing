def longest_collatz(limit):
    best, best_steps = 1, 0
    for start in range(1, limit + 1):
        n, steps = start, 0
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            steps += 1
        if steps > best_steps:
            best, best_steps = start, steps
    return best
