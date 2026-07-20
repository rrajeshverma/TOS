from datetime import time

from market.trading_session import TradingSession
from risk.circuit_breaker import CircuitBreaker


def test_trade_allowed_when_everything_is_healthy():
    session = TradingSession()
    breaker = CircuitBreaker()

    assert session.is_entry_allowed(time(10, 0))
    assert not breaker.is_tripped()


def test_trade_rejected_after_three_losses():
    session = TradingSession()
    breaker = CircuitBreaker()

    breaker.record_loss(100)
    breaker.record_loss(100)
    breaker.record_loss(100)

    assert session.is_entry_allowed(time(10, 0))
    assert breaker.is_tripped()


def test_trade_rejected_after_daily_loss_limit():
    session = TradingSession()
    breaker = CircuitBreaker()

    breaker.record_loss(5000)
    breaker.record_loss(5000)

    assert session.is_entry_allowed(time(11, 0))
    assert breaker.is_tripped()


def test_trade_rejected_before_entry_time():
    session = TradingSession()
    breaker = CircuitBreaker()

    assert not session.is_entry_allowed(time(9, 30))
    assert not breaker.is_tripped()


def test_trade_rejected_after_last_entry():
    session = TradingSession()
    breaker = CircuitBreaker()

    assert not session.is_entry_allowed(time(15, 0))
    assert not breaker.is_tripped()


def test_profit_resets_consecutive_losses():
    session = TradingSession()
    breaker = CircuitBreaker()

    breaker.record_loss(100)
    breaker.record_loss(100)
    breaker.record_profit(500)

    assert session.is_entry_allowed(time(10, 30))
    assert not breaker.is_tripped()


def test_force_exit_triggered():
    session = TradingSession()

    assert session.is_force_exit(time(15, 15))


def test_market_closed_blocks_trading():
    session = TradingSession()

    assert not session.is_market_open(time(16, 0))


def test_market_open_during_entry_window():
    session = TradingSession()

    assert session.is_market_open(time(11, 30))
    assert session.is_entry_allowed(time(11, 30))


def test_market_open_but_entries_closed():
    session = TradingSession()

    assert session.is_market_open(time(15, 10))
    assert not session.is_entry_allowed(time(15, 10))