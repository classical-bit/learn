import unittest


def bubble_sort(nums: list[int]) -> list[int]:
    swapping = True
    end = len(nums)
    while swapping:
        swapping = False
        for i in range(1, end):
            if nums[i - 1] > nums[i]:
                nums[i - 1], nums[i] = nums[i], nums[i - 1]
                swapping = True
        end -= 1

    return nums

arr = [1,89,5,6,4,3,75]

class TestBubbleSort(unittest.TestCase):
    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(arr), [1,3,4,5,6,75,89])

if __name__ == "__main__":
    unittest.main()
