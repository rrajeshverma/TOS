"""
Tests for MarketClock.
"""

from datetime import datetime

from runtime.market_clock import MarketClock
from runtime.session_state import SessionState


def create_time(
    hour: int,
    minute: int,
) -> datetime:
    return datetime(
        2026,
        8,
        3,
        hour,
        minute,
    )


def test_before_pre_open_is_closed():
    clock = MarketClock()

    assert clock.session_at(create_time(8, 59)) == SessionState.CLOSED


def test_pre_open_start():
    clock = MarketClock()

    assert clock.session_at(create_time(9, 0)) == SessionState.PRE_OPEN


def test_pre_open_end():
    clock = MarketClock()

    assert clock.session_at(create_time(9, 14)) == SessionState.PRE_OPEN


def test_market_open():
    clock = MarketClock()

    assert clock.session_at(create_time(9, 15)) == SessionState.OPEN


def test_midday():
    clock = MarketClock()

    assert clock.session_at(create_time(12, 0)) == SessionState.OPEN


def test_before_close():
    clock = MarketClock()

    assert clock.session_at(create_time(15, 29)) == SessionState.OPEN


def test_market_close():
    clock = MarketClock()

    assert clock.session_at(create_time(15, 30)) == SessionState.CLOSED


def test_evening():
    clock = MarketClock()

    assert clock.session_at(create_time(18, 0)) == SessionState.CLOSED
