def flip_and_invert_image(image: list[list[int]]) -> list[list[int]]:
    flipped = []
    for row in image:
        copy = []
        for i in range(len(row) - 1, -1, -1):
            copy.append(row[i])
        flipped.append(copy)
    for r in range(len(flipped)):
        for c in range(len(flipped[r])):
            flipped[r][c] = 0 if flipped[r][c] == 1 else 1
    return flipped
