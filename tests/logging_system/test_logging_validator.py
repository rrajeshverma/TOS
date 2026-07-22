import pytest

from config.config_manager import ConfigManager
from logging_system.logging_validator import LoggingValidator


def create_valid_config():
    return {
        "logging": {
            "level": "INFO",
            "directory": "logs",
            "filename": "tos.log",
            "rotation": "daily",
        }
    }


def test_valid_logging():
    validator = LoggingValidator(ConfigManager(create_valid_config()))
    assert validator.validate()


def test_missing_logging():
    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager({})).validate()


def test_missing_level():
    cfg = create_valid_config()
    del cfg["logging"]["level"]

    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager(cfg)).validate()


def test_missing_directory():
    cfg = create_valid_config()
    del cfg["logging"]["directory"]

    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager(cfg)).validate()


def test_missing_filename():
    cfg = create_valid_config()
    del cfg["logging"]["filename"]

    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager(cfg)).validate()


def test_missing_rotation():
    cfg = create_valid_config()
    del cfg["logging"]["rotation"]

    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager(cfg)).validate()


@pytest.mark.parametrize(
    "level",
    [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ],
)
def test_supported_levels(level):
    cfg = create_valid_config()
    cfg["logging"]["level"] = level

    assert LoggingValidator(ConfigManager(cfg)).validate()


def test_invalid_level():
    cfg = create_valid_config()
    cfg["logging"]["level"] = "TRACE"

    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager(cfg)).validate()


@pytest.mark.parametrize(
    "rotation",
    [
        "daily",
        "weekly",
        "monthly",
        "size",
    ],
)
def test_supported_rotation(rotation):
    cfg = create_valid_config()
    cfg["logging"]["rotation"] = rotation

    assert LoggingValidator(ConfigManager(cfg)).validate()


def test_invalid_rotation():
    cfg = create_valid_config()
    cfg["logging"]["rotation"] = "hourly"

    with pytest.raises(ValueError):
        LoggingValidator(ConfigManager(cfg)).validate()


def test_returns_true():
    validator = LoggingValidator(ConfigManager(create_valid_config()))
    assert validator.validate() is True


def test_multiple_runs():
    validator = LoggingValidator(ConfigManager(create_valid_config()))

    assert validator.validate()
    assert validator.validate()


def test_manager_not_modified():
    manager = ConfigManager(create_valid_config())

    LoggingValidator(manager).validate()

    assert manager.has("logging")