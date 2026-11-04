class ValidationError(Exception):
    """When the data inserted is invalid."""


class SchemaError(Exception):
    """When schema is defined wrongly."""