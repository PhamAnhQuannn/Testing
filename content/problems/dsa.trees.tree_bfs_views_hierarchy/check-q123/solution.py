def level_order(root):
    if not root:
        return []
    out, level = [], [root]
    while level:
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
