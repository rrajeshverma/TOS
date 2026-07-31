import pytest

from config.validators import (
    validate_range,
    validate_required,
    validate_type,
)


def test_validate_required_accepts_valid_value():
    assert validate_required("broker") is True


def test_validate_required_rejects_none():
    with pytest.raises(ValueError):
        validate_required(None)


def test_validate_required_rejects_empty_string():
    with pytest.raises(ValueError):
        validate_required("")


def test_validate_required_rejects_empty_list():
    with pytest.raises(ValueError):
        validate_required([])


def test_validate_required_rejects_empty_dict():
    with pytest.raises(ValueError):
        validate_required({})


def test_validate_type_accepts_string():
    assert validate_type("dhan", str) is True


def test_validate_type_accepts_integer():
    assert validate_type(10, int) is True


def test_validate_type_rejects_invalid_type():
    with pytest.raises(TypeError):
        validate_type("10", int)


def test_validate_type_accepts_float():
    assert validate_type(10.5, float) is True


def test_validate_type_accepts_boolean():
    assert validate_type(True, bool) is True


def test_validate_range_accepts_middle_value():
    assert validate_range(5, 1, 10) is True


def test_validate_range_accepts_lower_boundary():
    assert validate_range(1, 1, 10) is True


def test_validate_range_accepts_upper_boundary():
    assert validate_range(10, 1, 10) is True


def test_validate_range_rejects_below_minimum():
    with pytest.raises(ValueError):
        validate_range(0, 1, 10)


def test_validate_range_rejects_above_maximum():
    with pytest.raises(ValueError):
        validate_range(11, 1, 10)


def test_validate_range_accepts_float_values():
    assert validate_range(2.5, 1.0, 5.0) is True


def test_validate_range_rejects_negative_value():
    with pytest.raises(ValueError):
        validate_range(-1, 0, 10)


def test_validate_required_accepts_zero():
    assert validate_required(0) is True


def test_validate_required_accepts_false():
    assert validate_required(False) is True


def test_validate_required_accepts_non_empty_collection():
    assert validate_required([1]) is True
