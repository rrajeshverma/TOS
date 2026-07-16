from decimal import Decimal

from brokers.models import (
    Funds,
    Holding,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    Position,
    ProductType,
)


def test_create_order():
    order = Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=65,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    assert order.symbol == "NIFTY"
    assert order.side == OrderSide.BUY
    assert order.status == OrderStatus.PENDING


def test_create_position():
    position = Position(
        symbol="NIFTY",
        quantity=65,
        average_price=Decimal("250.50"),
        last_price=Decimal("252.00"),
        pnl=Decimal("112.50"),
    )

    assert position.quantity == 65


def test_create_holding():
    holding = Holding(
        symbol="SBIN",
        quantity=10,
        average_price=Decimal("800.00"),
    )

    assert holding.symbol == "SBIN"


def test_create_funds():
    funds = Funds(
        available_cash=Decimal("100000"),
        utilised_margin=Decimal("15000"),
        available_margin=Decimal("85000"),
    )

    assert funds.available_margin == Decimal("85000")


def test_order_side_enum():
    assert OrderSide.BUY.value == "BUY"
    assert OrderSide.SELL.value == "SELL"


def test_order_type_enum():
    assert OrderType.MARKET.value == "MARKET"


def test_default_order_status():
    order = Order(
        symbol="NIFTY",
        side=OrderSide.BUY,
        quantity=1,
        order_type=OrderType.MARKET,
        product=ProductType.INTRADAY,
    )

    assert order.status == OrderStatus.PENDING