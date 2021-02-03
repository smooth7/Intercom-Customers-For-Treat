import unittest

from distance import calculate_distance_km


class TestCalculateDistance(unittest.TestCase):

    def test_calculate_distance_1(self):
        self.assertEqual(calculate_distance_km(5, -5, 5, -5), 0)

    def test_calculate_distance_2(self):
        self.assertEqual(calculate_distance_km(53.339428, -6.257664, 51.999447, -9.742744), 278.2067221536354)


if __name__ == '__main__':
    unittest.main()
