import unittest 

from validator.validators import is_email, is_int, matches


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


if __name__ == "__main__":
    unittest.main()