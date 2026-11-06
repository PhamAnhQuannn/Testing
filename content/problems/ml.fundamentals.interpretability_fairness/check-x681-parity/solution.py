def parity_gap(a_approved, a_total, b_approved, b_total):
    rate_a = a_approved / a_total if a_total > 0 else 0.0
    rate_b = b_approved / b_total if b_total > 0 else 0.0
    return float(round(abs(rate_a - rate_b), 6))
