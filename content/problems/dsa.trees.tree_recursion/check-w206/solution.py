def good_nodes(r, mx=float("-inf")):
    if not r:
        return 0
    return (r.val >= mx) + good_nodes(r.left, max(mx, r.val)) + good_nodes(r.right, max(mx, r.val))
