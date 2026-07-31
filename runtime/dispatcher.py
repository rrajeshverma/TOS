from __future__ import annotations

from config.version import VERSION
from main import main as application_main
from runtime.health_monitor import HealthMonitor
from runtime.runtime_mode import RuntimeMode

from config.config_validator import ConfigValidator
from config.settings_loader import SettingsLoader

DEFAULT_CONFIG_PATH = "config/default.json"

class CommandDispatcher:
    def __init__(self) -> None:
        self._commands = {
            RuntimeMode.VERSION: self._version,
            RuntimeMode.HEALTH: self._health,
            RuntimeMode.VALIDATE: self._validate,
            RuntimeMode.PAPER: self._paper,
            RuntimeMode.LIVE: self._live,
        }

    def dispatch(self, mode: RuntimeMode) -> int:
        command = self._commands.get(mode)

        if command is None:
            print(f"Unsupported mode: {mode}")
            return 1

        return command()

    def _version(self) -> int:
        print(VERSION)
        return 0

    def _health(self) -> int:
        monitor = HealthMonitor()
        monitor.update()

        print(f"Healthy: {monitor.healthy}")
        print(f"Last Check: {monitor.last_check}")

        return 0

    def _validate(self) -> int:
            try:
                manager = SettingsLoader().load_json(DEFAULT_CONFIG_PATH)
                ConfigValidator(manager).validate()
                print("Configuration is valid.")
                return 0
            except Exception as exc:
                print(f"Configuration validation failed: {exc}")
                return 1

            
    def _paper(self) -> int:
        return application_main()


    def _live(self) -> int:
        print("Live mode not yet implemented.")
        return 0