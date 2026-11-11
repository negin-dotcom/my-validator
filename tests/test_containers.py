from collections import OrderedDict
import math
import unittest

from validator.containers import is_dict, is_list, is_none, is_set, is_tuple


GUARDS = {
    "list": is_list,
    "tuple": is_tuple,
    "set": is_set,
    "dict": is_dict,
    "none": is_none,
}

SAMPLES = {
    "list": [[], [0], [None], [math.inf]],
    "tuple": [(), (0,), (None,), (math.inf,)],
    "set": [set(), {0}, {None}, {math.inf}],
    "dict": [{}, dict(a=0), {0: ""}, {None: ""}, {math.inf: ""}],
    "none": [None],
    "other": [0, 2.5, "", b"abc", "abc", True, False, (1)],
}


class TestCollectionsValidator(unittest.TestCase):
    def test_each_guard_accepts_only_its_samples(self):
        for guard_name, guard in GUARDS.items():
            for sample_name, values in SAMPLES.items():
                expected = sample_name == guard_name 
                for value in values:
                    with self.subTest(guard=guard_name, value=value):
                        self.assertIs(guard(value), expected)

    def test_empties_are_accepted(self):
        self.assertIs(is_list([]), True)
        self.assertIs(is_tuple(()), True)
        self.assertIs(is_dict({}), True)
        self.assertIs(is_set(set()), True)

    def test_single_element_tuple_needs_trailing_comma(self):
        self.assertIs(is_tuple((1)), False)
        self.assertIs(is_tuple((1,)), True)

    def test_empty_curly_braces_are_a_dict_not_a_set(self):
        self.assertIs(is_dict({}), True)
        self.assertIs(is_set({}), False)

    def test_falsy_values_are_not_none(self):
        for value in [(), {}, [], 0.0, 0, True, False, set(), 
                      b"", ""]:
            with self.subTest(value=value):
                self.assertIs(is_none(value), False)

    def test_frozenset_is_not_a_set(self):
        self.assertIs(is_set(frozenset()), False)

    def test_dict_subclasses_are_dicts(self):
        self.assertIs(is_dict(OrderedDict()), True)



if __name__ == "__main__":
    unittest.main()