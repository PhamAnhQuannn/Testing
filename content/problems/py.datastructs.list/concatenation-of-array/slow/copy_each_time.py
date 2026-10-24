def get_concatenation(nums):
    ans = []
    for _ in range(2):
        for x in nums:
            ans = ans + [x]  # mỗi lần sao chép cả list: O(n^2)
    return ans
