import math
import unittest

from validator.collections import is_list, is_set, is_tuple


class TestCollectionsValidator(unittest.TestCase):
    def test_valid_set(self):
        for value in [{0}, {2}, {-1}, {1.8}, {-3.6}, 
                      {math.inf}, {""}, {None}]:
            with self.subTest(value=value):
                self.assertTrue(is_set(value))

    def test_invalid_set(self):
        self.assertFalse(is_set({}))

    def test_valid_list(self):
        for value in [[0], [2], [-1], [1.8], [-3.6], 
                      [math.inf], [""], [None], []]:
            with self.subTest(value=value):
                self.assertTrue(is_list(value))

    def test_valid_tuple(self):
        for value in [(0,), (2,), (-1,), (1.8,), (-3.6,), 
                      (math.inf,), ("",), (None,), ()]:
            with self.subTest(value=value):
                self.assertTrue(is_tuple(value))

    def test_tuple_with_a_single_element(self):
        self.assertIs(is_tuple((1,)), True)
        self.assertIs(is_tuple((1)), False)



if __name__ == "__main__":
    unittest.main()