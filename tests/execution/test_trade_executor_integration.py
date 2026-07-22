from decimal import Decimal

from execution.trade_executor import TradeExecutor
from services.position_manager import PositionManager

from tests.test_trade_factory import create_trade


def test_trade_executor_creates_position():

    executor = TradeExecutor(
        PositionManager()
    )

    trade = create_trade()

    position = executor.execute(
        trade,
        quantity=trade.quantity,
        price=trade.entry_price,
    )

    assert position.quantity == trade.quantity


def test_trade_executor_preserves_price():

    executor = TradeExecutor(
        PositionManager()
    )

    trade = create_trade()

    position = executor.execute(
        trade,
        quantity=trade.quantity,
        price=trade.entry_price,
    )

    assert position.average_price == trade.entry_price


def test_trade_executor_opens_position():

    executor = TradeExecutor(
        PositionManager()
    )

    trade = create_trade()

    position = executor.execute(
        trade,
        quantity=trade.quantity,
        price=Decimal("25000"),
    )

    assert position.is_open


def test_trade_executor_requires_trade():

    executor = TradeExecutor(
        PositionManager()
    )

    try:
        executor.execute(
            None,
            quantity=65,
            price=Decimal("25000"),
        )
        assert False
    except ValueError:
        assert True