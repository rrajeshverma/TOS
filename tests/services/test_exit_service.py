"""
Tests for Exit Service.
"""

from datetime import datetime, time
from decimal import Decimal
from unittest.mock import Mock

import pytest

from journal.trade_journal import TradeJournal

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.order import Order
from domain.position import Position
from domain.risk import Risk
from domain.trade import Trade
from services.exit_service import ExitService
from shared.enums import (
    Broker,
    DecisionStatus,
    ExitReason,
    OrderSide,
    OrderStatus,
    Signal,
    TradeStatus,
)
from utils.id_generator import (
    generate_decision_id,
    generate_order_id,
    generate_position_id,
    generate_trade_id,
)


@pytest.fixture
def isolated_journal(tmp_path):
    return TradeJournal(str(tmp_path / "trade_journal.csv"))


def create_service(journal):
    return ExitService(trade_journal=journal)


def create_position():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
    )

    indicators = IndicatorSet(
        ema_high=100,
        ema_low=90,
        vwap=100,
        rsi=60,
    )

    decision = Decision(
        decision_id=generate_decision_id(),
        timestamp=datetime.now(),
        market=market,
        indicator_set=indicators,
        signal=Signal.BUY_CE,
        status=DecisionStatus.VALID,
        reasons=("test",),
    )

    risk = Risk(
        decision=decision,
        approved=True,
        reasons=(),
    )

    trade = Trade(
        trade_id=generate_trade_id(),
        risk=risk,
        entry_price=Decimal(100),
        stop_loss=Decimal(90),
        target=Decimal(120),
        quantity=65,
        entry_time=datetime.now(),
        status=TradeStatus.OPEN,
    )

    order = Order(
        order_id=generate_order_id(),
        broker_order_id="BRK001",
        trade=trade,
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        quantity=65,
        requested_price=Decimal(100),
        status=OrderStatus.EXECUTED,
    )

    return Position(
        position_id=generate_position_id(),
        order=order,
        quantity=65,
        average_price=Decimal(100),
        last_traded_price=Decimal(100),
        status=TradeStatus.OPEN,
        opened_at=datetime.now(),
    )


def test_exit_service_closes_position_on_target(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(121),
        time(10, 0),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.TARGET
    assert result["position"].is_closed


def test_exit_service_closes_position_on_stop_loss(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(89),
        time(10, 0),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.STOP_LOSS
    assert result["position"].is_closed


def test_exit_service_closes_position_on_force_exit(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(105),
        time(15, 16),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.FORCE_EXIT
    assert result["position"].is_closed


def test_exit_service_keeps_position_open_when_no_exit(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(110),
        time(10, 0),
    )

    assert result["closed"] is False
    assert result["reason"] == ExitReason.NONE
    assert result["position"].is_open


def test_no_exit_does_not_return_trade(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(110),
        time(10, 0),
    )

    assert "trade" not in result


def test_closed_trade_status_is_closed(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(121),
        time(10, 0),
    )

    assert result["trade"].status == TradeStatus.CLOSED


def test_closed_trade_exit_price_set(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(121),
        time(10, 0),
    )

    assert result["trade"].exit_price == Decimal(121)


def test_closed_trade_exit_reason_set(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(89),
        time(10, 0),
    )

    assert result["trade"].exit_reason == ExitReason.STOP_LOSS


def test_profit_pnl_calculated(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(120),
        time(10, 0),
    )

    assert result["trade"].pnl == Decimal(1300)


def test_loss_pnl_calculated(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(90),
        time(10, 0),
    )

    assert result["trade"].pnl == Decimal(-650)


def test_trade_journal_called_once():
    journal = Mock()

    service = ExitService(
        trade_journal=journal,
    )

    position = create_position()

    service.evaluate(
        position,
        Decimal(121),
        time(10, 0),
    )

    journal.record.assert_called_once()


def test_trade_journal_not_called_when_no_exit():
    journal = Mock()

    service = ExitService(
        trade_journal=journal,
    )

    position = create_position()

    service.evaluate(
        position,
        Decimal(110),
        time(10, 0),
    )

    journal.record.assert_not_called()


def test_position_manager_called_once(isolated_journal):
    manager = Mock()

    closed_position = create_position()

    manager.close_position.return_value = closed_position
    manager.update_stop_loss.side_effect = lambda position, new_stop_loss: position

    service = ExitService(
        position_manager=manager,
        trade_journal=isolated_journal,
    )

    position = create_position()

    service.evaluate(
        position,
        Decimal(121),
        time(10, 0),
    )

    manager.update_stop_loss.assert_called_once_with(
        position,
        Decimal(100),
    )
    manager.close_position.assert_called_once_with(
        position,
        Decimal(121),
    )


def test_position_manager_not_called_when_no_exit(isolated_journal):
    manager = Mock()

    manager.update_stop_loss.side_effect = lambda position, new_stop_loss: position

    service = ExitService(
        position_manager=manager,
        trade_journal=isolated_journal,
    )

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(110),
        time(10, 0),
    )

    manager.update_stop_loss.assert_called_once_with(
        position,
        Decimal(100),
    )
    manager.close_position.assert_not_called()
    assert result["closed"] is False


def test_exit_manager_called_once(isolated_journal):
    exit_manager = Mock()
    exit_manager.check_exit.return_value = ExitReason.NONE

    position = create_position()

    updated_position = create_position()
    position_manager = Mock()
    position_manager.update_stop_loss.return_value = updated_position

    service = ExitService(
        exit_manager=exit_manager,
        position_manager=position_manager,
        trade_journal=isolated_journal,
    )

    service.evaluate(
        position,
        Decimal(110),
        time(10, 0),
    )

    position_manager.update_stop_loss.assert_called_once_with(
        position,
        Decimal(100),
    )
    exit_manager.check_exit.assert_called_once_with(
        updated_position,
        Decimal(110),
        time(10, 0),
    )


def test_closed_result_contains_trade(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(121),
        time(10, 0),
    )

    assert "trade" in result


def test_exit_service_moves_stop_loss_to_breakeven_at_one_r(isolated_journal):
    service = create_service(isolated_journal)

    position = create_position()

    result = service.evaluate(
        position,
        Decimal(110),
        time(10, 0),
    )

    assert result["closed"] is False
    assert result["position"].order.trade.stop_loss == Decimal(100)


def test_exit_service_uses_moved_stop_loss_for_exit(isolated_journal):
    position = create_position()

    management_engine = Mock()

    from domain.trade_management import TradeManagement

    management_engine.evaluate.return_value = TradeManagement(
        move_stop_loss=True,
        new_stop_loss=Decimal(100),
        exit_trade=False,
    )

    service = ExitService(
        trade_management_engine=management_engine,
        trade_journal=isolated_journal,
    )

    result = service.evaluate(
        position,
        Decimal(99),
        time(10, 0),
    )

    assert result["closed"] is True
    assert result["reason"] == ExitReason.STOP_LOSS
