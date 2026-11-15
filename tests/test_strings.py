import unittest
from functools import partial
import math
from fractions import Fraction
from decimal import Decimal

from validator.numbers import is_float, is_int
from validator.strings import (
    all_of, 
    any_of, 
    check_length, 
    is_email, 
    is_str, 
    matches, 
    max_length, 
    min_length,
    none_of,
    not_, 
    not_empty
)

NON_CALLABLES: list = [True, False, None, "0.0", 0, 0.0, dict(a=1),
                       {1}, (1,), [1], math.inf, float("nan"),
                       Fraction(1, 3), Decimal("1.5")]

def always_true(value):
    return True 


def always_false(value):
    return False 

def spy(result, calls):
    def check(value):
        calls.append(value)
        return result 

    return check


def raise_type_error(value):
    raise TypeError("wrong type")


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
        for value in ["", "a", "None", "0", "0.0", "-2", "{}", "()", "[]"]:
            with self.subTest(value=value):
                self.assertTrue(is_str(value))

    def test_invalid_str(self):
        for value in [(), [], {}, None, True, False, 0, 0.0, -2, b"abc"]:
            with self.subTest(value=value):
                self.assertFalse(is_str(value))

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


class TestCheckLengthValidator(unittest.TestCase):
    def test_check_length_with_other_than_min_length_and_max_length_raises(self):
        for bad_function in [str, bool, int, float, partial(min_length, minimum=3)]:
            with self.subTest(bad_function=bad_function):
                with self.assertRaisesRegex(ValueError, "min_length or max_length"):
                    check_length(bad_function, 3)


class TestAllOfValidator(unittest.TestCase):
    def test_empty_is_true(self):
        self.assertTrue(all_of()("anything"))

    def test_single_validator_matches_its_result(self):
        self.assertTrue(all_of(always_true)("anything"))
        self.assertFalse(all_of(always_false)("anything"))

    def test_passes_when_all_validators_pass(self):
        self.assertTrue(all_of(always_true, always_true)("anything"))

    def test_fails_when_any_validator_fails(self):
        for value_tuple in [(always_true, always_false), (always_false, always_false),
                            (always_false, always_true)]:
            with self.subTest(value_tuple=value_tuple):
                self.assertFalse(all_of(*value_tuple)("anything"))

    def test_short_circuit_with_one_result(self):
        calls = []
        result = all_of(spy(False, calls), spy(True, calls))
        self.assertFalse(result("anything"))
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls, ["anything"])

    def test_runs_every_validator_when_none_short_circuits(self):
        calls = []
        result = all_of(spy(True, calls), spy(True, calls))
        self.assertTrue(result("anything"))
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls, ["anything", "anything"])


class TestAnyOfValidator(unittest.TestCase):
    def test_empty_is_false(self):
        self.assertFalse(any_of()("anything"))

    def test_single_validator_matches_its_result(self):
        self.assertTrue(any_of(always_true)("anything"))
        self.assertFalse(any_of(always_false)("anything"))

    def test_fails_when_all_validators_fail(self):
        self.assertFalse(any_of(always_false, always_false)("anything"))

    def test_passes_when_any_validator_passes(self):
        for value_tuple in [(always_true, always_false), (always_true, always_true),
                             (always_false, always_true)]:
            with self.subTest(value_tuple=value_tuple):
                self.assertTrue(any_of(*value_tuple)("anything"))

    def test_short_circuit_with_one_result(self):
        calls = []
        result = any_of(spy(True, calls), spy(False, calls))
        self.assertTrue(result("anything"))
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls, ["anything"])

    def test_runs_every_validator_when_none_short_circuits(self):
        calls = []
        result = any_of(spy(False, calls), spy(False, calls))
        self.assertFalse(result("anything"))
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls, ["anything", "anything"])


class TestNotValidator(unittest.TestCase):
    def test_flips_true_to_false(self):
        self.assertFalse(not_(always_true)("anything"))

    def test_flips_false_to_true(self):
        self.assertTrue(not_(always_false)("anything"))

    def test_raises_on_non_callable(self):
        for validator in NON_CALLABLES:
            with self.subTest(validator=validator):
                with self.assertRaisesRegex(TypeError, "must be callable"):
                    not_(validator) 

    def test_odd_number_of_negations_is_the_same_as_first(self):
        result = not_(always_true)
        result_2 = not_(result)
        result_3 = not_(result_2)

        self.assertFalse(result("anything"))
        self.assertFalse(result_3("anything"))    

    def test_even_number_of_negations_is_the_flip_of_the_first(self):
        result = not_(always_true)
        result_2 = not_(result)

        self.assertFalse(result("anything"))
        self.assertTrue(result_2("anything"))

    def test_type_error_propagates(self):
        negated = not_(raise_type_error)
        with self.assertRaises(TypeError):
            negated("anything")

    def test_with_real_validator(self):
        self.assertTrue(not_(is_int)(1.0))
        self.assertFalse(not_(is_int)(1))


class TestNoneOfValidator(unittest.TestCase):
    def test_empty_is_true(self):
        self.assertTrue(none_of()("anything"))

    def test_single_validator_behaves_like_not_(self):
        self.assertTrue(none_of(always_false)("anything"))
        self.assertTrue(not_(always_false)("anything"))

        self.assertFalse(none_of(always_true)("anything"))
        self.assertFalse(not_(always_true)("anything"))

    def test_runs_all_validators_when_none_pass(self):
        calls = []
        result = none_of(spy(False, calls), spy(False, calls))
        self.assertTrue(result("anything"))
        self.assertEqual(len(calls), 2)

    def test_short_circuit_when_all_is_true(self):
        calls = []
        result = none_of(spy(True, calls), spy(True, calls))
        self.assertFalse(result("anything"))
        self.assertEqual(len(calls), 1)

    def test_runs_only_the_first_when_first_is_true(self):
        calls = []
        result = none_of(spy(True, calls), spy(False, calls))
        self.assertFalse(result("anything"))
        self.assertEqual(len(calls), 1)

    def test_runs_until_true_is_found(self):
        calls = []
        result = none_of(spy(False, calls), spy(False, calls), spy(True, calls),
                         spy(False, calls))
        self.assertFalse(result("anything"))
        self.assertEqual(len(calls), 3)

    def test_raises_on_non_callable(self):
        with self.assertRaisesRegex(TypeError, "must be callable"):
            none_of(NON_CALLABLES) 

    def test_type_error_propagates(self):
        negated = none_of(raise_type_error)
        with self.assertRaises(TypeError):
            negated("anything")

    def test_none_of_is_equal_to_not_any_of(self):
        none_of_result = none_of(is_int, is_float)
        not_any_of_result = not_(any_of(is_int, is_float))
        self.assertEqual(none_of_result("anything"),
                         not_any_of_result("anything"))



if __name__ == "__main__":
    unittest.main()