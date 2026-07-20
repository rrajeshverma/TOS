from datetime import time

from market.trading_session import TradingSession
from risk.circuit_breaker import CircuitBreaker


def test_trade_allowed_when_session_open_and_breaker_not_tripped():
    session = TradingSession()
    breaker = CircuitBreaker()

    current_time = time(10, 0)

    assert session.is_entry_allowed(current_time) is True
    assert breaker.is_tripped() is False


def test_trade_blocked_after_three_losses():
    session = TradingSession()
    breaker = CircuitBreaker()

    current_time = time(10, 0)

    breaker.record_loss(100)
    breaker.record_loss(100)
    breaker.record_loss(100)

    assert session.is_entry_allowed(current_time) is True
    assert breaker.is_tripped() is True


def test_trade_blocked_after_daily_loss_limit():
    session = TradingSession()
    breaker = CircuitBreaker()

    current_time = time(11, 30)

    breaker.record_loss(5000)
    breaker.record_loss(5000)

    assert session.is_entry_allowed(current_time) is True
    assert breaker.is_tripped() is True


def test_trade_blocked_before_entry_window():
    session = TradingSession()
    breaker = CircuitBreaker()

    current_time = time(9, 30)

    assert session.is_entry_allowed(current_time) is False
    assert breaker.is_tripped() is False


def test_trade_blocked_after_last_entry():
    session = TradingSession()
    breaker = CircuitBreaker()

    current_time = time(15, 0)

    assert session.is_entry_allowed(current_time) is False
    assert breaker.is_tripped() is False


def test_trade_allowed_after_profit_reset():
    session = TradingSession()
    breaker = CircuitBreaker()

    current_time = time(10, 30)

    breaker.record_loss(100)
    breaker.record_loss(100)
    breaker.record_profit(500)

    assert session.is_entry_allowed(current_time) is True
    assert breaker.is_tripped() is False


def test_force_exit_time_reached():
    session = TradingSession()

    assert session.is_force_exit(time(15, 15)) is True


def test_market_closed():
    session = TradingSession()

    assert session.is_market_open(time(16, 0)) is False


def test_market_open_and_entry_allowed():
    session = TradingSession()

    current_time = time(11, 0)

    assert session.is_market_open(current_time) is True
    assert session.is_entry_allowed(current_time) is True


def test_market_open_but_no_new_entries_after_last_entry():
    session = TradingSession()

    current_time = time(15, 10)

    assert session.is_market_open(current_time) is True
    assert session.is_entry_allowed(current_time) is False