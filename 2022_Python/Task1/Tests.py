import unittest

from Source import get_сoins_from_sum as tfunc


class TestMethod(unittest.TestCase):

    def test_default_set1(self):
        self.assertCountEqual(tfunc(231), [100, 100, 25, 5, 1])

    def test_default_set2(self):
        self.assertCountEqual(tfunc(15), [5, 10])

    def test_default_set3(self):
        self.assertCountEqual(tfunc(40), [5, 10, 25])

    def test_repeating_set(self):
        self.assertEqual(tfunc(50, [25, 5]), [25, 25])

    def test_negative_coin(self):
        self.assertEqual(tfunc(-1), [])

    def test_small_sum(self):
        self.assertEqual(tfunc(1, [5, 10, 25, 100]), [])


if __name__ == "__main__":
    unittest.main()