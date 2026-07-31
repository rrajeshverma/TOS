"""
TOS Production Dependency Checker

Validates required runtime dependencies.
"""

from __future__ import annotations


class DependencyChecker:
    """
    Checks production runtime dependencies.
    """

    def __init__(self) -> None:
        self._dependencies: dict[str, bool] = {}

    def register(
        self,
        name: str,
        available: bool,
    ) -> None:
        """
        Register dependency status.
        """

        self._dependencies[name] = available

    def is_ready(
        self,
    ) -> bool:
        """
        Check all dependencies.
        """

        if not self._dependencies:
            return False

        return all(self._dependencies.values())

    def missing(
        self,
    ) -> list[str]:
        """
        Return unavailable dependencies.
        """

        return [name for name, status in self._dependencies.items() if not status]

    def reset(
        self,
    ) -> None:
        """
        Clear dependency state.
        """

        self._dependencies.clear()
