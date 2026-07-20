from datetime import time

from market.trading_session import TradingSession


def test_default_times():
    session = TradingSession()

    assert session.entry_start == time(9, 45)
    assert session.last_entry == time(14, 45)
    assert session.force_exit == time(15, 15)


def test_entry_allowed():
    session = TradingSession()

    assert session.is_entry_allowed(time(10, 0)) is True


def test_before_entry():
    session = TradingSession()

    assert session.is_entry_allowed(time(9, 30)) is False


def test_after_last_entry():
    session = TradingSession()

    assert session.is_entry_allowed(time(15, 0)) is False


def test_force_exit_time():
    session = TradingSession()

    assert session.is_force_exit(time(15, 15)) is True


def test_before_force_exit():
    session = TradingSession()

    assert session.is_force_exit(time(15, 14)) is False


def test_market_open():
    session = TradingSession()

    assert session.is_market_open(time(10, 0)) is True


def test_market_closed_before():
    session = TradingSession()

    assert session.is_market_open(time(8, 0)) is False


def test_market_closed_after():
    session = TradingSession()

    assert session.is_market_open(time(15, 31)) is False


def test_summary():
    session = TradingSession()

    summary = session.summary()

    assert "entry_start" in summary
    assert "last_entry" in summary
    assert "force_exit" in summary


def test_custom_session():
    session = TradingSession(
        entry_start=time(10, 0),
        last_entry=time(14, 0),
        force_exit=time(15, 0),
    )

    assert session.entry_start == time(10, 0)


def test_entry_at_start():
    session = TradingSession()

    assert session.is_entry_allowed(time(9, 45)) is True


def test_entry_at_last():
    session = TradingSession()

    assert session.is_entry_allowed(time(14, 45)) is True


def test_force_exit_after():
    session = TradingSession()

    assert session.is_force_exit(time(15, 20)) is True


def test_market_close_boundary():
    session = TradingSession()

    assert session.is_market_open(time(15, 30)) is True