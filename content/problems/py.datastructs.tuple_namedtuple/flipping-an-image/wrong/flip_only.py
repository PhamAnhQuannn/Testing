def flip_and_invert_image(image: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in image]
