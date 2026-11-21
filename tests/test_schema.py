import unittest

from validator.combinators import all_of, check_length, optional
from validator.numbers import in_range_of, is_int
from validator.schema import Schema, validate
from validator.strings import is_str, max_length, min_length


def raises_type_error(value):
    raise TypeError("wrong type")

def raises_value_error(value):
    raise ValueError("bad configuration")


class TestSchemaValidator(unittest.TestCase):
    def setUp(self):
        self.fields = {
            "username": all_of(
                is_str, check_length(min_length, 5), check_length(max_length, 20)
            ),
            "age": all_of(is_int, in_range_of(18, 35)),
        }
        self.schema = Schema(self.fields)

    def test_with_min_age_all_data_is_validated_and_returns_empty_dict(self):
        data = {"username": "negin", "age": 18}
        self.assertEqual(validate(data, self.schema), {})

    def test_with_max_age_all_data_is_validated_and_returns_emptydict(self):
        data = {"username": "negin", "age": 35}
        self.assertEqual(validate(data, self.schema), {})

    def test_age_below_min_is_returned_with_message(self):
        data = {"username": "negin", "age": 17}
        self.assertEqual(
            validate(data, self.schema), {"age": self.schema.fields["age"].message}
        )

    def test_age_above_max_is_returned_with_message(self):
        data = {"username": "negin", "age": 36}
        self.assertEqual(
            validate(data, self.schema), {"age": self.schema.fields["age"].message}
        )

    def test_username_below_min_returns_empty_dict(self):
        data = {"username": "a" * 5, "age": 20}
        self.assertEqual(validate(data, self.schema), {})

    def test_username_above_max_returns_empty_dict(self):
        data = {"username": "a" * 20, "age": 20}
        self.assertEqual(validate(data, self.schema), {})

    def test_username_below_min_is_returned_with_message(self):
        data = {"username": "a" * 4, "age": 20}
        self.assertEqual(
            validate(data, self.schema), 
            {"username": self.schema.fields["username"].message}
        )

    def test_username_above_max_is_returned_with_message(self):
        data = {"username": "a" * 21, "age": 20}
        self.assertEqual(
            validate(data, self.schema), 
            {"username": self.schema.fields["username"].message}
        )

    def test_empty_data_returns_all_schema_fields(self):
        data = {}
        self.assertEqual(
            validate(data, self.schema),
            {"username": "is required", "age": "is required"},
        )

    def test_empty_schema_returns_empty_dict(self):
        fields = {}
        schema = Schema(fields)
        data = {"username": "negin", "age": 20}
        self.assertEqual(validate(data, schema), {})

    def test_extra_field_in_data_is_ignored(self):
        data = {"username": "negin", "age": 20, "password": 123456}
        self.assertEqual(validate(data, self.schema), {})

    def test_missing_field_in_data_is_returned(self):
        data = {"username": "negin"}
        self.assertEqual(validate(data, self.schema), {"age": "is required"})

    def test_several_fields_fail(self):
        data = {"username": "a" * 21, "age": 36}
        self.assertEqual(
            validate(data, self.schema),
            {
                "username": self.schema.fields["username"].message,
                "age": self.schema.fields["age"].message,
            },
        )

    def test_wrong_type_age_is_returned(self):
        data = {"username": "negin", "age": "20"}
        self.assertEqual(
            validate(data, self.schema), {"age": self.schema.fields["age"].message}
        )

    def test_wrong_type_username_is_returned(self):
        data = {"username": 1, "age": 20}
        self.assertEqual(
            validate(data, self.schema), 
            {"username": self.schema.fields["username"].message}
        )
    
    def test_type_error_reported_as_invalid_type(self):
        fields = {"username": raises_type_error}
        schema = Schema(fields)
        data = {"username": "negin"}

        self.assertEqual(
            validate(data, schema), {"username": "has an invalid type"}
        )

    def test_error_that_propagates(self):
        fields = {"username": raises_value_error}
        schema = Schema(fields)
        data = {"username": "negin"}

        with self.assertRaises(ValueError):
            validate(data, schema)


class TestExtraFieldsValidator(unittest.TestCase):
    def test_forbid_reports_every_extra_field(self):
        fields = {"username": is_str}
        schema = Schema(fields, extra_fields="forbid")
        data = {"username": "negin", "nickname": "n", "age": 30}

        self.assertEqual(
            validate(data, schema),
            {"nickname": "is not allowed", "age": "is not allowed"}
        )

    def test_invalid_type_with_extra_fields_as_forbid(self):
        fields = {"username": is_str}
        schema = Schema(fields, extra_fields="forbid")  
        data = {"username": 1}

        self.assertEqual(
            validate(data, schema), {"username": "must be a string"}
        )

    def test_missing_field_plus_extra_fields_as_forbid(self):
        fields = {"username": is_str, "nickname": is_str}
        schema = Schema(fields, extra_fields="forbid")  
        data = {"username": "negin", "age": 20}

        self.assertEqual(
            validate(data, schema), {"nickname": "is required", "age": "is not allowed"}
        )

class TestOptionalFields(unittest.TestCase):
    def test_missing_optional_is_skipped_but_missing_required_is_not(self):
        fields = {"name": is_str, "nickname": optional(is_str)}
        schema = Schema(fields)
        data = {}

        self.assertEqual(validate(data, schema), {"name": "is required"})


if __name__ == "__main__":
    unittest.main()
