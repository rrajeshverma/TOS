"""
Kill switch execution guard.
"""

from __future__ import annotations

from safety.kill_switch import KillSwitch


class KillSwitchGuard:
    """Execution guard backed by a kill switch."""

    def __init__(
        self,
        kill_switch: KillSwitch,
    ) -> None:
        self._kill_switch = kill_switch

    def can_execute(self) -> bool:
        """Return whether execution is allowed."""

        return not self._kill_switch.is_active()
