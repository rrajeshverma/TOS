from __future__ import annotations

from runtime.dispatcher import CommandDispatcher
from runtime.runtime_mode import RuntimeMode


class Launcher:
    def __init__(self):
        self._dispatcher = CommandDispatcher()

    def run(self, mode: RuntimeMode) -> int:
        return self._dispatcher.dispatch(mode)
