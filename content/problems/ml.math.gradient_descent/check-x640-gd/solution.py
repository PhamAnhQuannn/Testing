def gradient_descent(xs, ys, w0, lr, steps):
    w = w0
    n = len(xs)
    for _ in range(steps):
        grad = sum(2 * (w * x - y) * x for x, y in zip(xs, ys)) / n
        w = w - lr * grad
    return float(round(w, 6))
