def has_path_sum(r, t):
    if not r:
        return False
    if not r.left and (not r.right):
        return r.val == t
    return has_path_sum(r.left, t - r.val) or has_path_sum(r.right, t - r.val)
