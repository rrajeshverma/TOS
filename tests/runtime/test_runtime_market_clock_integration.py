"""
Tests for MarketClock integration with TradingRuntime.
"""

from unittest.mock import Mock

from runtime.session_state import SessionState
from runtime.trading_runtime import TradingRuntime


def create_runtime() -> TradingRuntime:
    runtime = TradingRuntime({})

    runtime.publish = Mock()
    runtime.run_cycle = Mock(return_value="OK")

    return runtime


def test_market_clock_updates_trading_session():
    runtime = create_runtime()

    runtime.market_clock.current_session = Mock(
        return_value=SessionState.OPEN,
    )

    runtime.on_market_tick(
        Mock(),
        [],
    )

    assert runtime.trading_session.state == SessionState.OPEN


def test_market_tick_ignored_when_market_closed():
    runtime = create_runtime()

    runtime.market_clock.current_session = Mock(
        return_value=SessionState.CLOSED,
    )

    runtime.on_market_tick(
        Mock(),
        [],
    )

    runtime.publish.assert_not_called()
    runtime.run_cycle.assert_not_called()


def test_market_tick_processed_when_market_open():
    runtime = create_runtime()

    runtime.market_clock.current_session = Mock(
        return_value=SessionState.OPEN,
    )

    market = Mock()

    result = runtime.on_market_tick(
        market,
        [],
    )

    runtime.run_cycle.assert_called_once_with(
        market,
        [],
    )

    assert result == "OK"


def test_market_tick_published_when_market_open():
    runtime = create_runtime()

    runtime.market_clock.current_session = Mock(
        return_value=SessionState.OPEN,
    )

    market = Mock()
    history = [market]

    runtime.on_market_tick(
        market,
        history,
    )

    runtime.publish.assert_called_once_with(
        runtime.publish.call_args.args[0],
        {
            "market": market,
            "history": history,
        },
    )
