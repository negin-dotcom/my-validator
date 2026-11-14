import math
import unittest
import sys
from decimal import Decimal
from fractions import Fraction

from validator.numbers import in_range, is_bool, is_float, is_int, is_negative, is_non_positive, is_number, is_positive


FLOATS: list = [-0.0, 0.0, 1.2, 10*1e6, 2/3, 1*2.3, 10*1e-6,
                sys.float_info.min, sys.float_info.max,
                float("nan"), math.inf, -math.inf]

INTS: list = [-10, 10, 0, 10**100]

POSITIVES: list = [2, 1.6, math.inf]

NEGATIVES: list = [-2, -1.6, -math.inf]


class TestIntValidator(unittest.TestCase):
    def test_ints_are_accepted(self):
        for value in INTS:
            with self.subTest(value=value):
                self.assertTrue(is_int(value))

    def test_non_ints_are_rejected(self):
        for value in [True, False, "10", 10.0, None, 10 + 10j, [10], {10}, (10,)]:
            with self.subTest(value=value):
                self.assertFalse(is_int(value))


class TestFloatValidator(unittest.TestCase):
    def test_floats_are_accepted(self):
        for value in FLOATS:
            with self.subTest(value=value):
                self.assertTrue(is_float(value))

    def test_non_floats_are_rejected(self):
        for value in [True, False, "0.0", 0, None, 10 + 10j, [0.0], {0.0}, (0.0,),
                      Decimal("1.5"), Fraction(1, 3)]:
            with self.subTest(value=value):
                self.assertFalse(is_float(value))


class TestNumberValidator(unittest.TestCase):
    def test_valid_numbers(self):
        for value in FLOATS + INTS:
            with self.subTest(value=value):
                self.assertTrue(is_number(value))

    def test_invalid_numbers(self):
        for value in [True, False, {0}, [0], (0,), 1 + 2j, "0", None,
                      Decimal("1.5"), Fraction(1, 3)]:
            with self.subTest(value=value):
                self.assertFalse(is_number(value))


class TestBoolValidator(unittest.TestCase):
    def test_valid_booleans(self):
        for value in [True, False]:
            with self.subTest(value=value):
                self.assertTrue(is_bool(value))

    def test_invalid_booleans(self):
        for value in FLOATS + INTS + [None, "1", (1,), [1], {1}, dict(a=1), 
                                      0, 1, 0.0]:
            with self.subTest(value=value):
                self.assertFalse(is_bool(value))


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
        for value in POSITIVES:
            with self.subTest(value=value):
                self.assertTrue(is_positive(value))

    def test_invalid_is_positive(self):
        for value in NEGATIVES + [0, -0.0, float("nan")]:
            with self.subTest(value=value):
                self.assertFalse(is_positive(value))

    def test_wrong_type_raises(self):
        for value in [None, True, False, "2", 4 + 2j, b"2",
                      Decimal("1.5"), Fraction(1, 3)]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    is_positive(value)


class TestIsNegativeValidator(unittest.TestCase):
    def test_valid_is_negative(self):
        for value in NEGATIVES:
            with self.subTest(value=value):
                self.assertTrue(is_negative(value))

    def test_invalid_is_negative(self):
        for value in POSITIVES + [0, 0.0, float("nan")]:
            with self.subTest(value=value):
                self.assertFalse(is_negative(value))
        
    def test_wrong_type_raises(self):
        for value in [None, True, False, "2", 4 + 2j, b"2",
                      Decimal("1.5"), Fraction(1, 3)]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    is_negative(value)


class TestIsNonPositive(unittest.TestCase):
    def test_valid_is_non_positive(self):
        for value in NEGATIVES + [0, 0.0, -0.0]:
            with self.subTest(value=value):
                self.assertTrue(is_non_positive(value))

    def test_invalid_is_non_positive(self):
        for value in POSITIVES + [float("nan")]:
            with self.subTest(value=value):
                self.assertFalse(is_non_positive(value))

    def test_wrong_type_raises(self):
        for value in [None, True, False, "2", 4 + 2j, b"2",
                        Decimal("1.5"), Fraction(1, 3)]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    is_non_positive(value)
    


if __name__ == "__main__":
    unittest.main()