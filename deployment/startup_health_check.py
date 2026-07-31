"""
TOS Startup Health Check

Validates system readiness before trading starts.
"""

from __future__ import annotations


class StartupHealthCheck:
    """
    Performs production startup checks.
    """

    def __init__(self) -> None:
        self._checks: dict[str, bool] = {}

    def register_check(
        self,
        name: str,
        status: bool,
    ) -> None:
        """
        Register startup check result.
        """

        self._checks[name] = status

    def is_ready(
        self,
    ) -> bool:
        """
        Return overall startup readiness.
        """

        if not self._checks:
            return False

        return all(self._checks.values())

    def failed_checks(
        self,
    ) -> list[str]:
        """
        Return failed health checks.
        """

        return [name for name, status in self._checks.items() if not status]

    def reset(
        self,
    ) -> None:
        """
        Clear health state.
        """

        self._checks.clear()
