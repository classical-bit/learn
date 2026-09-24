import unittest


def binary_search(target: int, arr: list[int]) -> bool:
    low = 0
    high = len(arr) - 1

    while low <= high:
        med = (low + high) // 2

        if  target == arr[med]:
            return True
        elif target > arr[med]:
            low = med + 1
        else:
            high = med - 1
    return False


array = [1,2,4,5,6,7,8,9,10,11,12,14,15,16,17]

class TestBinarySearch(unittest.TestCase):
    def test_bs_true(self):
        self.assertEqual(binary_search(17, array), True)

    def test_bs_false(self):
        self.assertEqual(binary_search(3, array), False)

if __name__ == "__main__":
    unittest.main()
