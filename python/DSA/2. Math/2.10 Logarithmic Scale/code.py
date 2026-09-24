import unittest
from math import log


def log_scale(data: list[float], base: float) -> list[float]:
    return [round(log(i, base)) for i in data]

class TestLogScale(unittest.TestCase):

    def test_log_scale_base_2(self):
        self.assertEqual(log_scale(
            [2, 4, 8, 16], 2),
            [1.0, 2.0, 3.0, 4.0])

    def test_log_scale_base_10(self):
        self.assertEqual(log_scale(
            [10, 100, 1000, 10000], 10),
            [1.0, 2.0, 3.0, 4.0])

if __name__ == "__main__":
    unittest.main()
