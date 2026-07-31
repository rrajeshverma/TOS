from __future__ import annotations

from config.config_manager import ConfigManager
from config.config_validator import ConfigValidator
from config.settings_loader import SettingsLoader


class RuntimeBootstrap:
    """Bootstrap runtime configuration."""

    def __init__(self) -> None:
        self._loader = SettingsLoader()

    def load_dict(self, data: dict) -> ConfigManager:
        manager = self._loader.load_dict(data)
        ConfigValidator(manager).validate()
        return manager

    def load_json(self, filename: str) -> ConfigManager:
        manager = self._loader.load_json(filename)
        ConfigValidator(manager).validate()
        return manager
