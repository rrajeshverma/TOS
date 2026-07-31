from __future__ import annotations

from config.config_manager import ConfigManager
from config.loader import load_dict as _load_dict
from config.loader import load_json as _load_json


class SettingsLoader:
    """Loads configuration into a ConfigManager."""

    def load_dict(self, data: dict) -> ConfigManager:
        manager = ConfigManager()
        manager.load(_load_dict(data))
        return manager

    def load_json(self, filename: str) -> ConfigManager:
        manager = ConfigManager()
        manager.load(_load_json(filename))
        return manager
