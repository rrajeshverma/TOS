import pytest

from config.config_manager import ConfigManager
from config.settings import Settings
from config.loader import load_dict, merge_configs
from config.validators import (
    validate_required,
    validate_type,
    validate_range,
)


# ---------------------------------------------------------------------
# ConfigManager
# ---------------------------------------------------------------------

def test_config_manager_initialization():
    manager = ConfigManager({"a": 1})
    assert manager.get("a") == 1


def test_config_manager_load():
    manager = ConfigManager()
    manager.load({"x": 10})
    assert manager.get("x") == 10


def test_config_manager_reload():
    manager = ConfigManager({"a": 1})
    manager.reload({"b": 2})
    assert manager.get("b") == 2


def test_config_manager_clear():
    manager = ConfigManager({"a": 1})
    manager.clear()
    assert manager.all() == {}


def test_config_manager_nested_lookup():
    manager = ConfigManager(
        {"database": {"host": "localhost"}}
    )
    assert manager.get("database.host") == "localhost"


def test_config_manager_missing_default():
    manager = ConfigManager()
    assert manager.get("missing", "default") == "default"


def test_config_manager_has():
    manager = ConfigManager({"x": 5})
    assert manager.has("x") is True


def test_config_manager_lock_unlock():
    manager = ConfigManager()

    manager.lock()

    with pytest.raises(RuntimeError):
        manager.set("a", 1)

    manager.unlock()
    manager.set("a", 1)

    assert manager.get("a") == 1


# ---------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------

def test_settings_set_get():
    settings = Settings()

    settings.set("mode", "paper")

    assert settings.get("mode") == "paper"


def test_settings_remove():
    settings = Settings({"mode": "paper"})

    settings.remove("mode")

    assert settings.has("mode") is False


def test_settings_clear():
    settings = Settings({"a": 1})

    settings.clear()

    assert settings.all() == {}


def test_settings_default():
    settings = Settings()

    assert settings.get("missing", 123) == 123


# ---------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------

def test_load_dict_returns_copy():
    data = {"risk": {"capital": 10000}}

    loaded = load_dict(data)

    assert loaded == data
    assert loaded is not data


def test_load_dict_invalid_type():
    with pytest.raises(TypeError):
        load_dict([])


def test_merge_configs_simple():
    left = {"a": 1}
    right = {"b": 2}

    merged = merge_configs(left, right)

    assert merged == {"a": 1, "b": 2}


def test_merge_configs_nested():
    left = {"risk": {"capital": 10000}}
    right = {"risk": {"max_loss": 500}}

    merged = merge_configs(left, right)

    assert merged["risk"]["capital"] == 10000
    assert merged["risk"]["max_loss"] == 500


# ---------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------

def test_validate_required_success():
    assert validate_required("hello") is True


def test_validate_required_none():
    with pytest.raises(ValueError):
        validate_required(None)


def test_validate_type_success():
    assert validate_type(10, int) is True


def test_validate_range_success():
    assert validate_range(50, 1, 100) is True