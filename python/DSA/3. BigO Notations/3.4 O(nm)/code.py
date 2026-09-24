import unittest


def get_avg_brand_followers(all_handles: list[list[str]], brand_name: str) -> float:
    count = 0
    for influencer_handles in all_handles:
        for handle in influencer_handles:
            if brand_name in handle:
                count = count + 1

    return round(count / len(all_handles), 2)

all_handles = [
    ["cosmofan1010", "cosmogirl", "billjane321"],
    ["cosmokiller", "gr8", "cosmojane3"],
    ["iloveboots", "paperthin"],
]
brand_name = "cosmo"

class TestAvgBrandFollowers(unittest.TestCase):
    def test_avg_brand_followers_cosmo(self):
        self.assertEqual(get_avg_brand_followers(all_handles, brand_name), 1.33)

if __name__ == "__main__":
    unittest.main()
