import math
import unittest
from decimal import Decimal
from fractions import Fraction

from validator.json_schema import from_json_schema
from validator.schema import validate


class TestJsonSchemaValidator(unittest.TestCase):
    def setUp(self):
        self.json_schema = {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "age": {"type": "integer"},
            },
        }
        
    def test_incorrect_data_with_json_schema(self):
        data = {"username": "negin", "age": "20"}

        self.assertEqual(
            validate(data, from_json_schema(self.json_schema)),
            {"age": "must be an integer"},
        )

    def test_correct_data_with_json_schema_returns_empty_dict(self):
        data = {"username": "negin", "age": 20}

        self.assertEqual(validate(data, from_json_schema(self.json_schema)), {})

    def test_wrong_type_in_json_schema_raises(self):
        json_schema = {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "age": {"type": "hey"},
            },
        }
        data = {"username": "negin", "age": 20}
        with self.assertRaisesRegex(ValueError, "hey"):
            validate(data, from_json_schema(json_schema))

    def test_json_schema_with_no_type_in_properties_passes(self):
        json_schema = {
            "type": "object",
            "properties": {
                "username": {},
            },
        }
        for value in ["hey", 0, 0.0, -2, math.inf, Decimal("1.5"),
                      Fraction(1, 3), float("nan"), b"abc", {}, [], 
                      dict(a=1), ()]:
        
            with self.subTest(value=value):
                data = {"username": value}
                self.assertEqual(validate(data, from_json_schema(json_schema)), {})

    def test_json_schema_with_no_properties_returns_empty_dict(self):
        json_schema = {"type": "object",}
        data = {"username": "negin"}
        self.assertEqual(validate(data, from_json_schema(json_schema)), {})

    def test_missing_field_in_json_schema_is_reported(self):
        data = {"username": "negin"}
        self.assertEqual(
            validate(data, from_json_schema(self.json_schema)),
            {"age": "is required"}
        )


if __name__ == "__main__":
    unittest.main()
