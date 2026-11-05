def life_step(b):
    R, Cc = (len(b), len(b[0]))

    def cnt(i, j):
        return (
            sum(
                (
                    b[x][y]
                    for x in range(max(0, i - 1), min(R, i + 2))
                    for y in range(max(0, j - 1), min(Cc, j + 2))
                )
            )
            - b[i][j]
        )

    return [
        [
            1 if b[i][j] and cnt(i, j) in (2, 3) or (not b[i][j] and cnt(i, j) == 3) else 0
            for j in range(Cc)
        ]
        for i in range(R)
    ]
