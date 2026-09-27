import unittest


def quick_sort(nums: list[int], low: int, high: int) -> None:
    if low < high:
        middle = partition(nums, low, high)
        quick_sort(nums, low, middle - 1)
        quick_sort(nums, middle + 1, high)


def partition(nums: list[int], low: int, high: int) -> int:
    pivot = nums[high]
    i = low - 1

    for j in range(low, high):
        if nums[j] < pivot:
            i += 1
            nums[i], nums[j] = nums[j], nums[i]

    nums[i + 1], nums[high] = nums[high], nums[i + 1]
    return i + 1


arr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
sorted_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class TestQuickSort(unittest.TestCase):
    def test_quick_sort(self):
        quick_sort(arr, 0, len(arr) - 1)
        self.assertEqual(arr, sorted_arr)

if __name__ == "__main__":
    unittest.main()
