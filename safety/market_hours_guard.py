"""
Market hours execution guard.
"""

from __future__ import annotations


class MarketHoursGuard:
    """Execution guard based on market status."""

    def __init__(self, market_open: bool = True) -> None:
        self._market_open = market_open

    def open_market(self) -> None:
        """Mark the market as open."""
        self._market_open = True

    def close_market(self) -> None:
        """Mark the market as closed."""
        self._market_open = False

    def can_execute(self) -> bool:
        """Return whether execution is allowed."""
        return self._market_open
