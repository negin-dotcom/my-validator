import math
import unittest

from validator.numbers import in_range, is_int, is_positive


class TestIntValidator(unittest.TestCase):
    def test_ints_are_accepted(self):
        for value in [-10, 10, 0, 10**100]:
            with self.subTest(value=value):
                self.assertTrue(is_int(value))

    def test_non_ints_are_rejected(self):
        for value in [True, False, "10", 10.0, None, 10 + 10j, [10], {10}, (10,)]:
            with self.subTest(value=value):
                self.assertFalse(is_int(value))



class TestInRangeValidator(unittest.TestCase):
    def test_valid_in_range(self):
        for value, low, high in [(2, 0, 5), (10.2, 0, 20), (6, 0.3, 8), 
                                 (9, 4, 12.6), (10.5, 8.7, 20.9), 
                                 (4, 2, 4), (3, 3, 3), (math.inf, 0, math.inf),
                                 (2, -math.inf, math.inf), (-2, -9, 0)]:
            with self.subTest(value=value, low=low, high=high):
                self.assertTrue(in_range(value, low, high))

    def test_invalid_in_range(self):
        for value, low, high in [(8, 0, 5), (4.5, 0, 3), (6, 2.5, 4), 
                                 (8, 3, 7.6), (2.2, 2.5, 2.8), (math.inf, -math.inf, 0),
                                 (-2, -3, -2.4), (5.001, 0, 5)]:
            with self.subTest(value=value, low=low, high=high):
                self.assertFalse(in_range(value, low, high))

    def test_wrong_type_raises(self):
        for value, low, high in [(3, 0, True), (3.2, False, 4), (True, 0, 5),
                                 ("2", 0, 4), (2, "0", 4), (2, 0, "4"),
                                 (2 + 2j, 0, 4), (None, -math.inf, math.inf)]:
            with self.subTest(value=value, low=low, high=high):
                with self.assertRaises(TypeError):
                    in_range(value, low, high)

    def test_low_greater_than_high(self):
        with self.assertRaises(ValueError):
            in_range(3, 5, 0)



class TestIsPositiveValidator(unittest.TestCase):
    def test_valid_is_positive(self):
        for value in [2, 1.6, math.inf]:
            with self.subTest(value=value):
                self.assertTrue(is_positive(value))

    def test_invalid_is_positive(self):
        for value in [-2, -1.7, -math.inf, 0, 0.0, -0.0, float("nan")]:
            with self.subTest(value=value):
                self.assertFalse(is_positive(value))

    def test_wrong_type_raises(self):
        for value in [None, True, False, "2", 4 + 2j, b"2"]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    is_positive(value)



if __name__ == "__main__":
    unittest.main()