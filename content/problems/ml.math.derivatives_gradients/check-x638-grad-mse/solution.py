def grad_mse(w, xs, ys):
    n = len(xs)
    total = 0.0
    for x, y in zip(xs, ys):
        total += 2 * (w * x - y) * x
    return round(total / n, 6)
