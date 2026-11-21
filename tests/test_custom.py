import unittest

from validator.custom import custom_validator


class TestCustomValidator(unittest.TestCase):
    def test_returns_func_result(self):
        is_even = custom_validator(lambda x: x % 2 == 0)
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(3))

    def test_has_code_and_message(self):
        f = custom_validator(lambda x: True, code="c", message="m")
        self.assertEqual(f.code, "c")
        self.assertEqual(f.message, "m")

    def test_non_callable_rejected(self):
        with self.assertRaises(TypeError):
            custom_validator(42)

    def test_non_string_code_raises(self):
        with self.assertRaisesRegex(TypeError, "must be string"):
            custom_validator(lambda x: True, code=42)

    def test_non_string_message_reaises(self):
        with self.assertRaisesRegex(TypeError, "must be string"):
            custom_validator(lambda x: True, message=42)

    def test_non_bool_result_raises(self):
        f = custom_validator(lambda x: None)
        with self.assertRaises(TypeError):
            f(42)

    def test_inner_exception_propagates(self):
        f = custom_validator(lambda x: x % 2 == 0)
        with self.assertRaises(TypeError):
            f("42")

    def test_defaults_from_function_name(self):
        def is_positive_even(x):
            return x > 0 and x % 2 == 0
        f = custom_validator(is_positive_even)
        self.assertEqual(f.code, "is_positive_even")
        self.assertIn("is_positive_even", f.message)


if __name__ == "__main__":
    unittest.main()
