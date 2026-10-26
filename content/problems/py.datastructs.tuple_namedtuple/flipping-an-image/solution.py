def flip_and_invert_image(image: list[list[int]]) -> list[list[int]]:
    result = []
    for row in image:
        new_row = []
        for v in row[::-1]:
            new_row.append(1 - v)
        result.append(new_row)
    return result
