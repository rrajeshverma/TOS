"""
Integration test:
Executed Order -> Position -> Trade Journal
"""

from datetime import datetime
from decimal import Decimal
from pathlib import Path

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.order_factory import OrderFactory
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory
from journal.trade_journal import TradeJournal
from services.position_manager import PositionManager
from shared.enums import Broker, OrderSide


def create_market():
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime(2026, 8, 18, 11, 0),
        open=22500,
        high=22550,
        low=22490,
        close=22540,
        volume=100000,
    )


def create_indicators():
    return IndicatorSet(
        ema_high=22500,
        ema_low=22450,
        vwap=22510,
        rsi=60,
        volume_average=90000,
    )


def create_trade():
    from engines.decision_engine import DecisionEngine

    decision = DecisionEngine().evaluate(
        create_market(),
        create_indicators(),
    )

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    return TradeFactory().create(
        risk,
        entry_price=Decimal(100),
        stop_loss=Decimal(90),
    )


def test_order_execution_creates_position():
    trade = create_trade()

    order = OrderFactory().create(
        trade,
        Broker.DHAN,
        OrderSide.BUY,
        Decimal(100),
    )

    position = PositionManager().open_position(
        order,
        order.quantity,
        Decimal(100),
    )

    assert position is not None
    assert position.order == order
    assert position.quantity == order.quantity
    assert position.is_open is True


def test_completed_trade_is_written_to_journal(
    tmp_path: Path,
):
    trade = create_trade()

    journal = TradeJournal(file_path=str(tmp_path / "trade_journal.csv"))

    journal.record(trade)

    assert journal.exists() is True
    assert journal.count() == 1


def test_position_contains_execution_price():
    trade = create_trade()

    order = OrderFactory().create(
        trade,
        Broker.DHAN,
        OrderSide.BUY,
        Decimal(100),
    )

    position = PositionManager().open_position(
        order,
        order.quantity,
        Decimal(100),
    )

    assert position.average_price == Decimal(100)
    assert position.last_traded_price == Decimal(100)


def test_journal_header_created(
    tmp_path: Path,
):
    journal_file = tmp_path / "journal.csv"

    journal = TradeJournal(file_path=str(journal_file))

    assert journal.exists() is True
    assert journal.count() == 0
