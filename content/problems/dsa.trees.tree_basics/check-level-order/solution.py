from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def level_order(flat):
    if not flat or flat[0] is None:
        return []
    root = TreeNode(flat[0])
    q = deque([root])
    i = 1
    while q and i < len(flat):
        node = q.popleft()
        if i < len(flat) and flat[i] is not None:
            node.left = TreeNode(flat[i])
            q.append(node.left)
        i += 1
        if i < len(flat) and flat[i] is not None:
            node.right = TreeNode(flat[i])
            q.append(node.right)
        i += 1
    out = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            n = q.popleft()
            level.append(n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        out.append(level)
    return out
