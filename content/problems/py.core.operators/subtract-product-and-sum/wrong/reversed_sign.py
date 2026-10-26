def subtract_product_and_sum(n: int) -> int:
    product = 1
    total = 0
    while n > 0:
        digit = n % 10
        product *= digit
        total += digit
        n //= 10
    return total - product
