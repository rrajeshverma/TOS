from config.config_manager import ConfigManager


def test_load_stores_configuration():
    manager = ConfigManager()

    manager.load({"broker": {"name": "paper"}})

    assert manager.get("broker.name") == "paper"


def test_reload_replaces_configuration():
    manager = ConfigManager({"broker": {"name": "old"}})

    manager.reload({"broker": {"name": "new"}})

    assert manager.get("broker.name") == "new"


def test_clear_removes_configuration():
    manager = ConfigManager({"broker": {"name": "paper"}})

    manager.clear()

    assert manager.all() == {}
