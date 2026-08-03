"""
Trading session manager.
"""

from runtime.session_state import SessionState


class TradingSession:
    """Controls trading session state."""

    def __init__(
        self,
        state: SessionState = SessionState.CLOSED,
    ) -> None:
        self._state = state

    @property
    def state(self) -> SessionState:
        """Current trading session."""

        return self._state

    def set_state(
        self,
        state: SessionState,
    ) -> None:
        """Update trading session."""

        self._state = state

    def current_state(self) -> SessionState:
        """Return current session."""

        return self._state

    def is_market_open(self) -> bool:
        """Return True when market is open."""

        return self._state == SessionState.OPEN

    def is_trading_allowed(self) -> bool:
        """Return True when trading is permitted."""

        return self._state == SessionState.OPEN

    def is_holiday(self) -> bool:
        """Return True on market holidays."""

        return self._state == SessionState.HOLIDAY

    def is_closed(self) -> bool:
        """Return True when market is closed."""

        return self._state == SessionState.CLOSED
