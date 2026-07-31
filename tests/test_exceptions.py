import pytest

from config.exceptions import (
    ConfigurationError,
    EnvironmentError,
    ValidationError,
)


def test_configuration_error_is_exception():
    assert issubclass(ConfigurationError, Exception)


def test_validation_error_is_exception():
    assert issubclass(ValidationError, Exception)


def test_environment_error_is_exception():
    assert issubclass(EnvironmentError, Exception)


def test_raise_configuration_error():
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("Configuration failed")


def test_raise_validation_error():
    with pytest.raises(ValidationError):
        raise ValidationError("Validation failed")


def test_raise_environment_error():
    with pytest.raises(EnvironmentError):
        raise EnvironmentError("Environment failed")


def test_configuration_error_message():
    with pytest.raises(ConfigurationError) as exc:
        raise ConfigurationError("Invalid configuration")

    assert str(exc.value) == "Invalid configuration"


def test_validation_error_message():
    with pytest.raises(ValidationError) as exc:
        raise ValidationError("Invalid value")

    assert str(exc.value) == "Invalid value"


def test_environment_error_message():
    with pytest.raises(EnvironmentError) as exc:
        raise EnvironmentError("Missing variable")

    assert str(exc.value) == "Missing variable"


def test_all_custom_exceptions_are_distinct():
    assert ConfigurationError != ValidationError
    assert ValidationError != EnvironmentError
    assert ConfigurationError != EnvironmentError
