"""
Tests for TradingSession.
"""

from runtime.session_state import SessionState
from runtime.trading_session import TradingSession


def test_default_state_is_closed() -> None:
    session = TradingSession()

    assert session.state == SessionState.CLOSED


def test_current_state() -> None:
    session = TradingSession(
        SessionState.OPEN,
    )

    assert session.current_state() == SessionState.OPEN


def test_set_state() -> None:
    session = TradingSession()

    session.set_state(
        SessionState.OPEN,
    )

    assert session.state == SessionState.OPEN


def test_market_open() -> None:
    session = TradingSession(
        SessionState.OPEN,
    )

    assert session.is_market_open()


def test_market_not_open() -> None:
    session = TradingSession(
        SessionState.CLOSED,
    )

    assert not session.is_market_open()


def test_trading_allowed() -> None:
    session = TradingSession(
        SessionState.OPEN,
    )

    assert session.is_trading_allowed()


def test_trading_not_allowed_closed() -> None:
    session = TradingSession(
        SessionState.CLOSED,
    )

    assert not session.is_trading_allowed()


def test_trading_not_allowed_holiday() -> None:
    session = TradingSession(
        SessionState.HOLIDAY,
    )

    assert not session.is_trading_allowed()


def test_holiday() -> None:
    session = TradingSession(
        SessionState.HOLIDAY,
    )

    assert session.is_holiday()


def test_not_holiday() -> None:
    session = TradingSession(
        SessionState.OPEN,
    )

    assert not session.is_holiday()


def test_closed() -> None:
    session = TradingSession(
        SessionState.CLOSED,
    )

    assert session.is_closed()


def test_not_closed() -> None:
    session = TradingSession(
        SessionState.OPEN,
    )

    assert not session.is_closed()
