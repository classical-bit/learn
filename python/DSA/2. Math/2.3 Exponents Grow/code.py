import unittest


def get_follower_prediction(
    follower_count: int, influencer_type: str, num_months: int
) -> int:
    multipliers = {
        "fitness": 4,
        "cosmetic": 3
    }

    r = multipliers.get(influencer_type.lower(), 2)
    return int(follower_count * (r ** num_months))

class TestFollowerPrediction(unittest.TestCase):

    def test_fitness_influencer(self):
        self.assertEqual(get_follower_prediction(10, "fitness", 2), 160)

    def test_cosmetic_influencer(self):
        self.assertEqual(get_follower_prediction(10, "cosmetic", 2), 90)

    def test_other_influencer(self):
        self.assertEqual(get_follower_prediction(10, "gaming", 2), 40)

    def test_zero_months(self):
        self.assertEqual(get_follower_prediction(100, "fitness", 0), 100)

    def test_zero_followers(self):
        self.assertEqual(get_follower_prediction(0, "cosmetic", 5), 0)

if __name__ == "__main__":
    unittest.main()
