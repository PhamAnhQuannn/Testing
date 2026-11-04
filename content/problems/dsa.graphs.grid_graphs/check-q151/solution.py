def flood_fill(img, sr, sc, color):
    old = img[sr][sc]
    if old == color:
        return img
    st = [(sr, sc)]
    while st:
        r, c = st.pop()
        if 0 <= r < len(img) and 0 <= c < len(img[0]) and (img[r][c] == old):
            img[r][c] = color
            st += [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return img
