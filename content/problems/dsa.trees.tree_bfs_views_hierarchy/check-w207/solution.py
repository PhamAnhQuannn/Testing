def avg_levels(root):
    if not root:
        return []
    out, level = [], [root]
    while level:
        out.append(sum(n.val for n in level) / len(level))
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
