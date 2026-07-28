"""
TOS Execution Mode Control

Controls whether trading runs in:
- PAPER mode
- LIVE mode
"""

from enum import Enum


class ExecutionMode(Enum):
    """
    Trading execution modes.
    """

    PAPER = "PAPER"
    LIVE = "LIVE"


class ExecutionModeGuard:
    """
    Safety gate before order execution.
    """

    def __init__(
        self,
        mode: ExecutionMode = ExecutionMode.PAPER,
    ) -> None:

        self._mode = mode
        self._live_enabled = False


    @property
    def mode(self) -> ExecutionMode:

        return self._mode


    def enable_live_trading(self) -> None:
        """
        Explicitly enable live trading.
        """

        self._live_enabled = True


    def disable_live_trading(self) -> None:
        """
        Emergency disable.
        """

        self._live_enabled = False


    def can_execute(self) -> bool:
        """
        Check execution permission.
        """

        if self._mode == ExecutionMode.PAPER:
            return True

        return self._live_enabled


    def set_mode(
        self,
        mode: ExecutionMode,
    ) -> None:

        self._mode = mode
