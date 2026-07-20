def validate_required(value):
    """
    Validate that a required value is present.
    """
    if value is None:
        raise ValueError("Value is required.")

    if isinstance(value, str) and value == "":
        raise ValueError("Value cannot be empty.")

    if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
        raise ValueError("Collection cannot be empty.")

    return True


def validate_type(value, expected_type):
    """
    Validate the type of a value.
    """
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Expected {expected_type.__name__}, got {type(value).__name__}"
        )

    return True


def validate_range(value, minimum, maximum):
    """
    Validate that a numeric value falls within the specified range.
    """
    if value < minimum:
        raise ValueError(
            f"Value {value} is less than minimum {minimum}"
        )

    if value > maximum:
        raise ValueError(
            f"Value {value} is greater than maximum {maximum}"
        )

    return True