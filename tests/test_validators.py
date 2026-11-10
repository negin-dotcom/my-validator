import math
import unittest 

from validator.validators import in_range, is_email, is_int, is_positive, matches, max_length, min_length


class TestRegexValidator(unittest.TestCase):
    def test_number_only_fullmatch(self):
        self.assertTrue(matches("123", r"\d+"))

    def test_alpha_only_fullmatch(self):
        self.assertTrue(matches("abc", r"\w+"))

    def test_alpha_with_whitespace_fullmatch(self):
        self.assertTrue(matches("hey def", r"\w+\s+\w+"))



class TestIntValidator(unittest.TestCase):
    def test_ints_are_accepted(self):
        for value in [-10, 10, 0, 10**100]:
            with self.subTest(value=value):
                self.assertTrue(is_int(value))

    def test_non_ints_are_rejected(self):
        for value in [True, False, "10", 10.0, None, 10 + 10j, [10], {10}, (10,)]:
            with self.subTest(value=value):
                self.assertFalse(is_int(value))



class TestEmailValidator(unittest.TestCase):
    def test_valid_emails(self):
        for email in ["john@example.com", "john+-.doe@google.com"]:
            with self.subTest(email=email):
                self.assertTrue(is_email(email))

    def test_invalid_emails(self):
        for email in ["john@-@@example.com", "google.com", "john doe@example.com",
                      "@example.com"]:
            with self.subTest(email=email):
                self.assertFalse(is_email(email))

    def test_wrong_type_emails(self):
        for email in [None, 1234, b"john.doe@example.com"]:
            with self.subTest(email=email):
                with self.assertRaises(TypeError):
                    is_email(email)



class TestMinLengthValidator(unittest.TestCase):
    def test_accepts(self):
        for value, minimum in [("abc", 3), ("abc", 2), ("abc", 1), ("abc", 0),
                               ("", 0)]:
            with self.subTest(value=value, minimum=minimum):
                self.assertTrue(min_length(value, minimum))

    def test_rejects(self):
        for value, minimum in [("abc", 4), ("", 1)]:
            with self.subTest(value=value, minimum=minimum):
                self.assertFalse(min_length(value, minimum))

    def test_minimum_negative_value(self):
        with self.assertRaises(ValueError):
            min_length("abc", -1)

    def test_wrong_type_raises(self):
        for value, minimum in [(10, 2), (10.5, 2), ("abc", 3.5), 
                               ("abc", "3"), ("abc", True)]:
            with self.subTest(value=value, minimum=minimum):
                with self.assertRaises(TypeError):
                    min_length(value, minimum)



class TestMaxLengthValidator(unittest.TestCase):
    def test_accepts(self):
        for value, maximum in [("abc", 3), ("abc", 4), ("abc", 5), ("", 0)]:
            with self.subTest(value=value, maximum=maximum):
                self.assertTrue(max_length(value, maximum))

    def test_rejects(self):
        for value, maximum in [("abc", 2), ("abc", 1), ("abc", 0)]:
            with self.subTest(value=value, maximum=maximum):
                self.assertFalse(max_length(value, maximum))

    def test_wrong_type_raises(self):
        for value, maximum in [(10, 3), (10.5, 3), ("abc", 3.5), 
                               ("abc", "3"), ("abc", True)]:
            with self.subTest(value=value, maximum=maximum):
                with self.assertRaises(TypeError):
                    max_length(value, maximum)

    def test_maximum_negative_value(self):
        with self.assertRaises(ValueError):
            max_length("abc", -1)


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