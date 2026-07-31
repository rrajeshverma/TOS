from __future__ import annotations

from config.version import VERSION
from main import main as application_main
from runtime.health_monitor import HealthMonitor
from runtime.runtime_mode import RuntimeMode


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
        print("Configuration validation entry point.")
        return 0

    def _paper(self) -> int:
        return application_main()

    def _live(self) -> int:
        print("Live mode not yet implemented.")
        return 0
