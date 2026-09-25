import unittest


def insertion_sort(nums: list[int]) -> list[int]:
    for j in range(1, len(nums)):
        while j > 0:
            if nums[j - 1] > nums[j]:
                nums[j - 1], nums[j] = nums[j], nums[ j - 1]
            j -= 1
    return nums


arr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
sorted_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class TestInsertionSort(unittest.TestCase):
    def test_insertion_sort(self):
        self.assertEqual(insertion_sort(arr), sorted_arr)

if __name__ == "__main__":
    unittest.main()
