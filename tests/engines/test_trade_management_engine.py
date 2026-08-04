from decimal import Decimal

from engines.trade_management_engine import (
    TradeManagementEngine,
)


def test_move_stop_to_breakeven():
    engine = TradeManagementEngine()

    result = engine.evaluate(
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        current_price=Decimal("110"),
    )

    assert result.move_stop_loss
    assert result.new_stop_loss == Decimal("100")


def test_do_not_move_before_one_r():
    engine = TradeManagementEngine()

    result = engine.evaluate(
        entry_price=Decimal("100"),
        stop_loss=Decimal("90"),
        current_price=Decimal("105"),
    )

    assert not result.move_stop_loss
    assert result.new_stop_loss is None
