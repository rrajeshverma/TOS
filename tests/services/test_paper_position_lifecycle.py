from datetime import time
from decimal import Decimal
from types import SimpleNamespace

from services.paper_position_lifecycle import PaperPositionLifecycle


def test_successful_execution_opens_position():
    risk = SimpleNamespace(is_approved=True)

    trade_plan = SimpleNamespace(
        position_size=SimpleNamespace(quantity=65),
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24900"),
    )

    execution_result = SimpleNamespace(
        success=True,
    )

    lifecycle = PaperPositionLifecycle()

    position = lifecycle.open_from_execution(
        risk=risk,
        trade_plan=trade_plan,
        execution_result=execution_result,
    )

    assert position is not None
    assert position.quantity == 65
    assert position.average_price == Decimal("25000")
    assert position.is_open
    assert lifecycle.position_book.count() == 1
    assert position.order is not None


def test_failed_execution_does_not_open_position():
    risk = SimpleNamespace(is_approved=True)

    trade_plan = SimpleNamespace(
        position_size=SimpleNamespace(quantity=65),
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24900"),
    )

    execution_result = SimpleNamespace(
        success=False,
    )

    lifecycle = PaperPositionLifecycle()

    position = lifecycle.open_from_execution(
        risk=risk,
        trade_plan=trade_plan,
        execution_result=execution_result,
    )

    assert position is None
    assert lifecycle.position_book.count() == 0


def test_update_positions_keeps_open_position_and_updates_price(tmp_path):
    from decimal import Decimal

    from journal.trade_journal import TradeJournal

    risk = SimpleNamespace(is_approved=True)

    trade_plan = SimpleNamespace(
        position_size=SimpleNamespace(quantity=65),
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24900"),
    )

    execution_result = SimpleNamespace(success=True)

    lifecycle = PaperPositionLifecycle(
        trade_journal=TradeJournal(str(tmp_path / "journal.csv")),
    )

    position = lifecycle.open_from_execution(
        risk=risk,
        trade_plan=trade_plan,
        execution_result=execution_result,
    )

    results = lifecycle.update_positions(
        current_price=Decimal("25050"),
        current_time=time(14, 30),
    )
    assert results[0]["closed"] is False

    updated = lifecycle.position_book.get_position(position.position_id)

    assert updated.last_traded_price == Decimal("25050")
    assert updated.is_open


def test_update_positions_closes_target_and_records_journal(tmp_path):
    from decimal import Decimal

    from journal.trade_journal import TradeJournal

    risk = SimpleNamespace(is_approved=True)

    trade_plan = SimpleNamespace(
        position_size=SimpleNamespace(quantity=65),
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24900"),
    )

    execution_result = SimpleNamespace(success=True)

    journal = TradeJournal(str(tmp_path / "journal.csv"))

    lifecycle = PaperPositionLifecycle(
        trade_journal=journal,
    )

    position = lifecycle.open_from_execution(
        risk=risk,
        trade_plan=trade_plan,
        execution_result=execution_result,
    )

    results = lifecycle.update_positions(
        current_price=Decimal("25200"),
    )

    assert results[0]["closed"] is True
    assert not lifecycle.position_book.contains(position.position_id)
    assert journal.count() == 1
    assert journal.daily_pnl() == Decimal("13000")


def test_open_from_execution_synchronizes_order_fill(tmp_path):
    from decimal import Decimal
    from unittest.mock import Mock

    from journal.trade_journal import TradeJournal

    risk = SimpleNamespace(is_approved=True)

    trade_plan = SimpleNamespace(
        position_size=SimpleNamespace(quantity=65),
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24900"),
    )

    execution_result = SimpleNamespace(
        success=True,
        order_id=1,
    )

    order_service = Mock()
    order_service.broker_order_id.return_value = "BROKER-1"

    broker = Mock()

    lifecycle = PaperPositionLifecycle(
        trade_journal=TradeJournal(str(tmp_path / "journal.csv")),
        order_service=order_service,
        broker=broker,
    )

    position = lifecycle.open_from_execution(
        risk=risk,
        trade_plan=trade_plan,
        execution_result=execution_result,
    )

    assert position.is_open

    order_service.record_fill.assert_called_once_with(
        1,
        quantity=65,
        price=25000.0,
    )
    order_service.broker_order_id.assert_called_once_with(1)
    broker.modify_order.assert_called_once()
