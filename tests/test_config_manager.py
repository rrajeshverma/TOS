import pytest

from config.config_manager import ConfigManager


def test_create_empty_config_manager():
    config = ConfigManager()

    assert config.all() == {}
    assert config.is_locked() is False


def test_create_config_manager_with_initial_data():
    config = ConfigManager({"broker": "dhan"})

    assert config.get("broker") == "dhan"


def test_load_configuration_from_dictionary():
    config = ConfigManager()

    config.load({"risk": {"max_loss": 1000}})

    assert config.get("risk.max_loss") == 1000


def test_reload_configuration():
    config = ConfigManager({"broker": "old"})

    config.reload({"broker": "new"})

    assert config.get("broker") == "new"


def test_clear_configuration():
    config = ConfigManager({"broker": "dhan"})

    config.clear()

    assert config.all() == {}


def test_get_existing_key():
    config = ConfigManager({"broker": "dhan"})

    assert config.get("broker") == "dhan"


def test_get_missing_key_returns_none():
    config = ConfigManager()

    assert config.get("missing") is None


def test_get_missing_key_with_default():
    config = ConfigManager()

    assert config.get("missing", "default") == "default"


def test_get_nested_key_using_dot_notation():
    config = ConfigManager(
        {
            "risk": {
                "capital": 10000,
            }
        }
    )

    assert config.get("risk.capital") == 10000


def test_has_existing_key():
    config = ConfigManager({"broker": "dhan"})

    assert config.has("broker") is True


def test_has_missing_key():
    config = ConfigManager({"broker": "dhan"})

    assert config.has("strategy") is False


def test_set_new_configuration_value():
    config = ConfigManager()

    config.set("broker", "dhan")

    assert config.get("broker") == "dhan"


def test_update_existing_configuration_value():
    config = ConfigManager({"broker": "old"})

    config.set("broker", "new")

    assert config.get("broker") == "new"


def test_default_value_is_not_saved():
    config = ConfigManager()

    config.get("broker", "dhan")

    assert config.has("broker") is False


def test_get_all_configuration_values():
    data = {
        "broker": "dhan",
        "capital": 10000,
    }

    config = ConfigManager(data)

    assert config.all() == data


def test_lock_configuration():
    config = ConfigManager()

    config.lock()

    assert config.is_locked() is True


def test_cannot_modify_locked_configuration():
    config = ConfigManager()

    config.lock()

    with pytest.raises(RuntimeError):
        config.set("broker", "dhan")


def test_unlock_configuration():
    config = ConfigManager()

    config.lock()
    config.unlock()

    assert config.is_locked() is False


def test_is_locked_returns_true_after_lock():
    config = ConfigManager()

    config.lock()

    assert config.is_locked()


def test_is_locked_returns_false_by_default():
    config = ConfigManager()

    assert not config.is_locked()
