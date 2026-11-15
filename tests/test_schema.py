import unittest

from validator.combinators import all_of, check_length
from validator.numbers import in_range_of, is_int
from validator.schema import validate
from validator.strings import is_str, max_length, min_length 


def raises_type_error(value):
    raise TypeError("wrong type")


class TestSchemaValidator(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "username": all_of(is_str, 
                               check_length(min_length, 5), 
                               check_length(max_length, 20)),
                               
            "age": all_of(is_int,
                          in_range_of(18, 35)),
        }

    def test_with_min_age_all_data_is_validated_and_returns_empty_dict(self):
        data = {
            "username": "negin",
            "age": 18
        }
        self.assertEqual(validate(data, self.schema), {})

    def test_with_max_age_all_data_is_validated_and_returns_emptydict(self):
        data = {
            "username": "negin",
            "age": 35
        }
        self.assertEqual(validate(data, self.schema), {})

    def test_age_below_min_is_returned_with_message(self):
        data = {
            "username": "negin",
            "age": 17
        }
        self.assertEqual(validate(data, self.schema),
                         {"age": self.schema["age"].message})

    def test_age_above_max_is_returned_with_message(self):
        data = {
            "username": "negin",
            "age": 36
        }
        self.assertEqual(validate(data, self.schema),
                         {"age": self.schema["age"].message})

    def test_username_below_min_returns_empty_dict(self):
        data = {
            "username": "a" * 5,
            "age": 20
        }
        self.assertEqual(validate(data, self.schema), {})

    def test_username_above_max_returns_empty_dict(self):
        data = {
            "username": "a" * 20,
            "age": 20
        }
        self.assertEqual(validate(data, self.schema), {})

    def test_username_below_min_is_returned_with_message(self):
        data = {
            "username": "a" * 4,
            "age": 20
        }
        self.assertEqual(validate(data, self.schema), 
                         {"username": self.schema["username"].message})

    def test_username_above_max_is_returned_with_message(self):
        data = {
            "username": "a" * 21,
            "age": 20
        }
        self.assertEqual(validate(data, self.schema),
                         {"username": self.schema["username"].message})

    def test_empty_data_returns_all_schema_fields(self):
        data = {}
        self.assertEqual(validate(data, self.schema),
                         {"username": "is required",
                          "age": "is required"})

    def test_empty_schema_returns_empty_dict(self):
        schema = {}
        data = {
            "username": "negin",
            "age": 20
        }
        self.assertEqual(validate(data, schema), {})

    def test_extra_field_in_data_is_ignored(self):
        data = {
            "username": "negin",
            "age": 20,
            "password": 123456
        }
        self.assertEqual(validate(data, self.schema), {})

    def test_missing_field_in_data_is_returned(self):
        data = {
            "username": "negin"
        }
        self.assertEqual(validate(data, self.schema), 
                         {"age": "is required"})

    def test_several_fields_fail(self):
        data = {
            "username": "a" * 21,
            "age": 36
        }
        self.assertEqual(validate(data, self.schema), 
                         {"username": self.schema["username"].message,
                          "age": self.schema["age"].message})

    def test_wrong_type_age_is_returned(self):
        data = {
            "username": "negin",
            "age": "20"
        }
        self.assertEqual(validate(data, self.schema), 
                         {"age": self.schema["age"].message})

    def test_wrong_type_username_is_returned(self):
        data = {
            "username": 1,
            "age": 20
        }
        self.assertEqual(validate(data, self.schema), 
                         {"username": self.schema["username"].message})
        
    def test_error_that_propagates(self):
        schema = {
            "username": raises_type_error
        }
        data = {
            "username": "negin",
        }

        with self.assertRaises(TypeError):
            validate(data, schema)
            


if __name__ == "__main__":
    unittest.main()