def can_jump(nums):
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
        if reach >= len(nums) - 1:
            return True
    return True
