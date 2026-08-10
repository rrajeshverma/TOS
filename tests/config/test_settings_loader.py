import json

import pytest

from config.config_manager import ConfigManager
from config.settings_loader import SettingsLoader


def test_load_from_dict_returns_config_manager():
    loader = SettingsLoader()

    manager = loader.load_dict(
        {
            "broker": {"name": "DHAN"},
            "runtime": {"mode": "PAPER"},
        }
    )

    assert isinstance(manager, ConfigManager)
    assert manager.get("broker.name") == "DHAN"
    assert manager.get("runtime.mode") == "PAPER"


def test_load_dict_rejects_non_dictionary():
    loader = SettingsLoader()

    with pytest.raises(TypeError):
        loader.load_dict("invalid")


def test_load_json(tmp_path):
    config = {
        "broker": {"name": "DHAN"},
        "runtime": {"mode": "PAPER"},
    }

    filename = tmp_path / "config.json"
    filename.write_text(json.dumps(config))

    loader = SettingsLoader()

    manager = loader.load_json(filename)

    assert manager.get("broker.name") == "DHAN"
    assert manager.get("runtime.mode") == "PAPER"
