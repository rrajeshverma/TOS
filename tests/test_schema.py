import pytest

from config.schema import (
    create_schema,
    has_field,
    validate_schema,
)


def test_create_empty_schema():
    assert create_schema() == {}


def test_create_schema_with_fields():
    schema = create_schema(
        broker=str,
        capital=int,
    )

    assert "broker" in schema
    assert "capital" in schema


def test_has_existing_field():
    schema = create_schema(broker=str)

    assert has_field(schema, "broker")


def test_has_missing_field():
    schema = create_schema()

    assert not has_field(schema, "risk")


def test_validate_valid_schema():
    schema = create_schema(
        broker=str,
        capital=int,
    )

    data = {
        "broker": "dhan",
        "capital": 10000,
    }

    assert validate_schema(schema, data)


def test_validate_missing_field():
    schema = create_schema(broker=str)

    with pytest.raises(KeyError):
        validate_schema(schema, {})


def test_validate_invalid_type():
    schema = create_schema(capital=int)

    with pytest.raises(TypeError):
        validate_schema(schema, {"capital": "100"})


def test_validate_string():
    schema = create_schema(name=str)

    assert validate_schema(schema, {"name": "Rajesh"})


def test_validate_integer():
    schema = create_schema(capital=int)

    assert validate_schema(schema, {"capital": 100})


def test_validate_float():
    schema = create_schema(risk=float)

    assert validate_schema(schema, {"risk": 2.5})


def test_validate_boolean():
    schema = create_schema(debug=bool)

    assert validate_schema(schema, {"debug": True})


def test_validate_multiple_fields():
    schema = create_schema(
        broker=str,
        capital=int,
        debug=bool,
    )

    assert validate_schema(
        schema,
        {
            "broker": "dhan",
            "capital": 10000,
            "debug": False,
        },
    )


def test_schema_returns_dictionary():
    assert isinstance(create_schema(), dict)


def test_validate_empty_schema():
    assert validate_schema({}, {})


def test_schema_field_count():
    schema = create_schema(
        a=int,
        b=int,
        c=int,
    )

    assert len(schema) == 3


def test_has_field_returns_false_for_empty_schema():
    assert not has_field({}, "broker")


def test_validate_extra_fields_allowed():
    schema = create_schema(name=str)

    assert validate_schema(
        schema,
        {
            "name": "Rajesh",
            "age": 35,
        },
    )


def test_schema_contains_expected_type():
    schema = create_schema(capital=int)

    assert schema["capital"] is int


def test_validate_nested_dictionary_value():
    schema = create_schema(config=dict)

    assert validate_schema(schema, {"config": {}})


def test_validate_list_value():
    schema = create_schema(symbols=list)

    assert validate_schema(schema, {"symbols": []})
