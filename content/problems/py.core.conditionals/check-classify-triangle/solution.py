def classify_triangle(a, b, c):
    x, y, z = sorted((a, b, c))
    if x <= 0 or x + y <= z:
        return "invalid"
    if x == y == z:
        kind = "equilateral"
    elif x == y or y == z:
        kind = "isosceles"
    else:
        kind = "scalene"
    if x * x + y * y == z * z:
        kind += " right"
    return kind
