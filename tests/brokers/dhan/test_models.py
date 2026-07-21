from brokers.dhan.models import (
    BrokerAccount,
    BrokerOrder,
    BrokerPosition,
)


def test_broker_order_creation():
    order = BrokerOrder(
        symbol="NIFTY",
        side="BUY",
        quantity=50,
        order_type="MARKET",
        price=None,
    )

    assert order.symbol == "NIFTY"
    assert order.side == "BUY"
    assert order.quantity == 50
    assert order.order_type == "MARKET"
    assert order.price is None


def test_broker_position_creation():
    position = BrokerPosition(
        symbol="BANKNIFTY",
        quantity=25,
        average_price=245.75,
    )

    assert position.symbol == "BANKNIFTY"
    assert position.quantity == 25
    assert position.average_price == 245.75


def test_broker_account_creation():
    account = BrokerAccount(
        client_id="client123",
        available_margin=125000.50,
        utilized_margin=25000.00,
    )

    assert account.client_id == "client123"
    assert account.available_margin == 125000.50
    assert account.utilized_margin == 25000.00

from datetime import datetime

from brokers.dhan.models import BrokerTick


def test_broker_tick_creation():
    now = datetime.now()

    tick = BrokerTick(
        symbol="NIFTY",
        ltp=25100.50,
        volume=1200,
        timestamp=now,
    )

    assert tick.symbol == "NIFTY"
    assert tick.ltp == 25100.50
    assert tick.volume == 1200
    assert tick.timestamp == now