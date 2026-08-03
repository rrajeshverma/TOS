"""
Market clock.

Determines the current trading session.
"""

from __future__ import annotations

from datetime import datetime, time

from runtime.session_state import SessionState


class MarketClock:
    """Determines the trading session."""

    PRE_OPEN = time(9, 0)
    MARKET_OPEN = time(9, 15)
    MARKET_CLOSE = time(15, 30)

    def session_at(
        self,
        now: datetime,
    ) -> SessionState:
        """Return the trading session for a given time."""

        current = now.time()

        if current < self.PRE_OPEN:
            return SessionState.CLOSED

        if current < self.MARKET_OPEN:
            return SessionState.PRE_OPEN

        if current < self.MARKET_CLOSE:
            return SessionState.OPEN

        return SessionState.CLOSED

    def current_session(self) -> SessionState:
        """Return current trading session."""

        return self.session_at(
            datetime.now(),
        )
