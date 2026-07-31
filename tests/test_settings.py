from config.settings import (
    Settings,
)


def test_create_empty_settings():
    settings = Settings()

    assert settings.all() == {}


def test_create_settings_with_initial_values():
    settings = Settings({"broker": "dhan"})

    assert settings.get("broker") == "dhan"


def test_set_new_setting():
    settings = Settings()

    settings.set("capital", 10000)

    assert settings.get("capital") == 10000


def test_update_existing_setting():
    settings = Settings({"capital": 10000})

    settings.set("capital", 20000)

    assert settings.get("capital") == 20000


def test_get_missing_setting_returns_default():
    settings = Settings()

    assert settings.get("risk", 2) == 2


def test_has_existing_setting():
    settings = Settings({"broker": "dhan"})

    assert settings.has("broker")


def test_has_missing_setting():
    settings = Settings()

    assert not settings.has("broker")


def test_remove_existing_setting():
    settings = Settings({"broker": "dhan"})

    settings.remove("broker")

    assert not settings.has("broker")


def test_clear_settings():
    settings = Settings({"broker": "dhan"})

    settings.clear()

    assert settings.all() == {}


def test_all_returns_dictionary():
    settings = Settings()

    assert isinstance(settings.all(), dict)


def test_setting_count():
    settings = Settings(
        {
            "a": 1,
            "b": 2,
        }
    )

    assert len(settings.all()) == 2


def test_overwrite_multiple_values():
    settings = Settings({"a": 1})

    settings.set("a", 2)
    settings.set("b", 3)

    assert settings.get("a") == 2
    assert settings.get("b") == 3


def test_remove_missing_setting():
    settings = Settings()

    settings.remove("missing")

    assert settings.all() == {}


def test_store_boolean_value():
    settings = Settings()

    settings.set("debug", True)

    assert settings.get("debug") is True


def test_store_float_value():
    settings = Settings()

    settings.set("risk", 2.5)

    assert settings.get("risk") == 2.5
