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
