def flip_and_invert_image(image: list[list[int]]) -> list[list[int]]:
    return [[1 - v for v in row] for row in image]
