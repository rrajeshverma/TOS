"""
Emergency kill switch.
"""

from __future__ import annotations


class KillSwitch:
    """Emergency trading kill switch."""

    def __init__(self) -> None:
        self._active = False

    def activate(self) -> None:
        """Activate the kill switch."""

        self._active = True

    def deactivate(self) -> None:
        """Deactivate the kill switch."""

        self._active = False

    def is_active(self) -> bool:
        """Return kill switch status."""

        return self._active
