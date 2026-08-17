"""
Composite execution guard.
"""

from __future__ import annotations

from collections.abc import Iterable


class CompositeExecutionGuard:
    """Combines multiple execution guards."""

    def __init__(self, guards: Iterable) -> None:
        self._guards = tuple(guards)

    def can_execute(self) -> bool:
        """Return True only if every guard allows execution."""

        return all(guard.can_execute() for guard in self._guards)

    def record_execution(self) -> None:
        """Record a successfully submitted execution on supporting guards."""

        for guard in self._guards:
            record = getattr(guard, "record_execution", None)

            if record is not None:
                record()
