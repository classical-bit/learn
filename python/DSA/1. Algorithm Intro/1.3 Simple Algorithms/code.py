from functools import reduce


def summed(nums: list[int]) -> int:
    return reduce(lambda total, item: total + item, nums, 0)

print(summed([1,2,3,4]))
# 10
