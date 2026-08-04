"""
Tests for TradeExecutor.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pytest

from domain.indicator_set import IndicatorSet
from domain.market import Market
from backtesting.trade_executor import TradeExecutor
from domain.decision import Decision
from domain.risk import Risk
from shared.enums import (
    DecisionStatus,
    ExitReason,
    Signal,
    TradeStatus,
)


def create_risk(
    signal: Signal = Signal.BUY_CE,
) -> Risk:
    """
    Create an approved Risk object for testing.
    """

    market = Market(
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="30m",
        timestamp=datetime.now(),
        open=100.0,
        high=105.0,
        low=95.0,
        close=102.0,
        volume=1000,
    )

    indicators = IndicatorSet(
        ema_high=101.0,
        ema_low=99.0,
        vwap=100.0,
        rsi=60.0,
        volume_average=1000.0,
    )

    decision = Decision(
        decision_id="D1",
        timestamp=datetime.now(),
        market=market,
        indicator_set=indicators,
        signal=signal,
        status=DecisionStatus.VALID,
        reasons=(),
    )

    return Risk(
        decision=decision,
        approved=True,
        reasons=(),
    )


def test_open_trade():
    executor = TradeExecutor()

    trade = executor.open_trade(
        risk=create_risk(),
        entry_price=Decimal("100"),
        quantity=1,
        entry_time=datetime.now(),
    )

    assert trade.status == TradeStatus.OPEN
    assert executor.has_open_trade
    assert executor.current_trade == trade


def test_cannot_open_second_trade():
    executor = TradeExecutor()

    executor.open_trade(
        risk=create_risk(),
        entry_price=Decimal("100"),
        quantity=1,
        entry_time=datetime.now(),
    )

    with pytest.raises(RuntimeError):
        executor.open_trade(
            risk=create_risk(),
            entry_price=Decimal("110"),
            quantity=1,
            entry_time=datetime.now(),
        )


def test_close_buy_trade_profit():
    executor = TradeExecutor()

    executor.open_trade(
        risk=create_risk(Signal.BUY_CE),
        entry_price=Decimal("100"),
        quantity=2,
        entry_time=datetime.now(),
    )

    trade = executor.close_trade(
        exit_price=Decimal("110"),
        exit_time=datetime.now(),
        exit_reason=ExitReason.TARGET,
    )

    assert trade.status == TradeStatus.CLOSED
    assert trade.pnl == Decimal("20")
    assert executor.current_trade is None
    assert not executor.has_open_trade


def test_close_pe_trade_profit():
    executor = TradeExecutor()

    executor.open_trade(
        risk=create_risk(Signal.BUY_PE),
        entry_price=Decimal("100"),
        quantity=2,
        entry_time=datetime.now(),
    )

    trade = executor.close_trade(
        exit_price=Decimal("90"),
        exit_time=datetime.now(),
        exit_reason=ExitReason.TARGET,
    )

    assert trade.pnl == Decimal("20")


def test_close_without_open_trade():
    executor = TradeExecutor()

    with pytest.raises(RuntimeError):
        executor.close_trade(
            exit_price=Decimal("100"),
            exit_time=datetime.now(),
        )
