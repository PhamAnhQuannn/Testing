def smaller_numbers_than_current(nums: list[int]) -> list[int]:
    answer = []
    for i in range(len(nums)):
        count = 0
        for j in range(len(nums)):
            if j != i and nums[j] < nums[i]:
                count += 1
        answer.append(count)
    return answer
