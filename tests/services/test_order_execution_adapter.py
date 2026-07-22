from decimal import Decimal

from engines.order_factory import OrderFactory
from tests.test_trade_factory import create_trade
from shared.enums import Broker, OrderSide


def create_order():

    return OrderFactory().create(
        trade=create_trade(),
        broker=Broker.DHAN,
        side=OrderSide.BUY,
        price=Decimal("25000"),
    )


def test_adapter_converts_domain_order():

    from services.order_execution_adapter import (
        OrderExecutionAdapter,
    )

    adapter = OrderExecutionAdapter()

    result = adapter.to_execution_order(
        create_order()
    )

    assert result["symbol"] == "NIFTY"


def test_adapter_quantity():

    from services.order_execution_adapter import (
        OrderExecutionAdapter,
    )

    result = OrderExecutionAdapter().to_execution_order(
        create_order()
    )

    assert result["quantity"] == 65


def test_adapter_side():

    from services.order_execution_adapter import (
        OrderExecutionAdapter,
    )

    result = OrderExecutionAdapter().to_execution_order(
        create_order()
    )

    assert result["side"] == "BUY"


def test_adapter_price():

    from services.order_execution_adapter import (
        OrderExecutionAdapter,
    )

    result = OrderExecutionAdapter().to_execution_order(
        create_order()
    )

    assert result["price"] == 25000.0