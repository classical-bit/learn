import unittest


def selection_sort(nums: list[int]) -> list[int]:
    for i in range(len(nums)):
        smallest_idx = i

        for j in range(i + 1, len(nums)):
            if nums[j] < nums[smallest_idx]:
                smallest_idx = j

        nums[i], nums[smallest_idx] = nums[smallest_idx], nums[i]

    return nums


arr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
sorted_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class TestSelectionSort(unittest.TestCase):
    def test_selection_sort(self):
        self.assertEqual(selection_sort(arr), sorted_arr)

if __name__ == "__main__":
    unittest.main()
