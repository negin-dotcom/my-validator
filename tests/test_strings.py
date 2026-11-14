import unittest
from functools import partial

from validator.strings import check_length, is_email, is_str, matches, max_length, min_length, not_empty


class TestRegexValidator(unittest.TestCase):
    def test_number_only_fullmatch(self):
        self.assertTrue(matches("123", r"\d+"))

    def test_alpha_only_fullmatch(self):
        self.assertTrue(matches("abc", r"\w+"))

    def test_alpha_with_whitespace_fullmatch(self):
        self.assertTrue(matches("hey def", r"\w+\s+\w+"))


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


class TestStrValidator(unittest.TestCase):
    def test_valid_str(self):
        for value in ["", "a", "None", "0", "0.0", "-2", "{}", "()", "[]",
                      '', 'a', 'None', '0', '0.0', '-2', '{}', '()', '[]']:
            with self.subTest(value=value):
                self.assertTrue(is_str(value))

    def test_rejects_not_empty(self):
        for value in ["", " "]:
            with self.subTest(value=value):
                self.assertFalse(not_empty(value))

    def test_accepts_not_empty(self):
        for value in ["a", "a b", " a", " a ", "a "]:
            with self.subTest(value=value):
                self.assertTrue(not_empty(value))

    def test_wrong_type_raises(self):
        for value in [None, 0, 0.0, -1, 1 + 2j, (1,), {1}, 
                      dict(a=1), [1], True, False]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    not_empty(value)

    def test_check_length_with_other_than_min_length_and_max_length_raises(self):
        for bad_function in [str, bool, int, float, partial(min_length, n=3)]:
            with self.subTest(bad_function=bad_function):
                with self.assertRaisesRegex(ValueError, "min_length or max_length"):
                    check_length(bad_function, 3)

     

if __name__ == "__main__":
    unittest.main()