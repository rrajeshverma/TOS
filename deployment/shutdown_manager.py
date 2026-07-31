"""
TOS Runtime Shutdown Manager

Handles safe application shutdown.
"""

from __future__ import annotations


class ShutdownManager:
    """
    Controls graceful shutdown lifecycle.
    """

    def __init__(self) -> None:
        self._shutdown = False
        self._steps: list[str] = []

    def execute(
        self,
    ) -> list[str]:
        """
        Execute shutdown sequence.
        """

        if self._shutdown:
            return self._steps

        self._steps = [
            "stop_orders",
            "close_session",
            "save_state",
            "flush_journal",
            "release_resources",
        ]

        self._shutdown = True

        return self._steps

    def is_shutdown(
        self,
    ) -> bool:
        """
        Return shutdown status.
        """

        return self._shutdown

    def completed_steps(
        self,
    ) -> list[str]:
        """
        Return completed shutdown steps.
        """

        return list(self._steps)

    def reset(
        self,
    ) -> None:
        """
        Reset shutdown state.
        """

        self._shutdown = False
        self._steps.clear()
