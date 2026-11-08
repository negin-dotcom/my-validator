import unittest 

from validator.validators import matches


class TestRegexValidator(unittest.TestCase):
    def test_number_only_fullmatch(self):
        self.assertTrue(matches("123", r"\d+"))

    def test_alpha_only_fullmatch(self):
        self.assertTrue(matches("abc", r"\w+"))

    def test_alpha_with_whitespace_fullmatch(self):
        self.assertTrue(matches("hey def", r"\w+\s+\w+"))



if __name__ == "__main__":
    unittest.main()