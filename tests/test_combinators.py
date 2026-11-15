from decimal import Decimal
from fractions import Fraction
import math
import unittest
from functools import partial

from validator.combinators import (
    all_of, 
    any_of, 
    check_length, 
    none_of, 
    not_
)

from validator.numbers import is_float, is_int
from validator.strings import min_length


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