def winner(board):
    lines = []
    for i in range(3):
        lines.append([board[i][0], board[i][1], board[i][2]])
        lines.append([board[0][i], board[1][i], board[2][i]])
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])
    for mark in ("X", "O"):
        for line in lines:
            if line[0] == mark and line[1] == mark and line[2] == mark:
                return mark
    for row in board:
        if "." in row:
            return "none"
    return "draw"
