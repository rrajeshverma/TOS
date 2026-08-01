"""
Reconnect policy.
"""

from __future__ import annotations


class ReconnectPolicy:
    """Reconnect retry policy."""

    def __init__(self, max_attempts: int = 3) -> None:
        self._attempts = 0
        self._max_attempts = max_attempts

    def can_retry(self) -> bool:
        return self._attempts < self._max_attempts

    def record_failure(self) -> None:
        if self.can_retry():
            self._attempts += 1

    def reset(self) -> None:
        self._attempts = 0

    @property
    def attempts(self) -> int:
        return self._attempts
