import unittest


def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) < 2:
        return nums

    mid = len(nums) // 2

    left_sorted = merge_sort(nums[:mid])
    right_sorted = merge_sort(nums[mid:])

    return merge(left_sorted, right_sorted)

def merge(first: list[int], second: list[int]) -> list[int]:
    a = 0
    b = 0
    final = []

    while a < len(first) and b < len(second):
        if first[a] < second[b]:
            final.append(first[a])
            a = a + 1
        else:
            final.append(second[b])
            b = b + 1

    while a < len(first):
        final.append(first[a])
        a = a + 1

    while b < len(second):
        final.append(second[b])
        b = b + 1

    return final

arr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
sorted_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class TestMergeSort(unittest.TestCase):
    def test_merge_sort(self):
        self.assertEqual(merge_sort(arr), sorted_arr)

    def test_merge_sort_edge(self):
        self.assertEqual(merge_sort([1]), [1])

    def test_merge(self):
        self.assertEqual(merge([1,2,3], [4,5,6]), [1,2,3,4,5,6])

if __name__ == "__main__":
    unittest.main()
