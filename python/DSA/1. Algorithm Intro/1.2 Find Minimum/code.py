def find_minimum(nums: list[int]) -> float | None:
    if len(nums) == 0:
        return None

    minimum = float("inf")
    for num in nums:
        minimum = min(minimum, num)

    return minimum

print(find_minimum([1,2,3,4,5,6,7,8,0]))
# 0
