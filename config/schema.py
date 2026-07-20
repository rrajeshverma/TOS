def create_schema(**fields):
    """
    Create a schema definition.
    """
    return dict(fields)


def has_field(schema, field):
    """
    Check if a field exists in the schema.
    """
    return field in schema


def validate_schema(schema, data):
    """
    Validate data against a schema.
    """
    for field, expected_type in schema.items():
        if field not in data:
            raise KeyError(f"Missing required field: {field}")

        if not isinstance(data[field], expected_type):
            raise TypeError(
                f"Field '{field}' must be of type "
                f"{expected_type.__name__}"
            )

    return True