def zigzag(root):
    if not root:
        return []
    out, level, ltr = [], [root], True
    while level:
        vals = [n.val for n in level]
        out.append(vals if ltr else vals[::-1])
        ltr = not ltr
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
