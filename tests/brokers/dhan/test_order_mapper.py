import pytest

from brokers.dhan.order_mapper import OrderMapper


def test_maps_buy_market_order():
    mapper = OrderMapper()

    payload = mapper.to_broker_order(
        symbol="NIFTY",
        side="BUY",
        quantity=50,
        order_type="MARKET",
    )

    assert payload == {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 50,
        "order_type": "MARKET",
    }


def test_maps_sell_limit_order():
    mapper = OrderMapper()

    payload = mapper.to_broker_order(
        symbol="BANKNIFTY",
        side="SELL",
        quantity=25,
        order_type="LIMIT",
        price=250.50,
    )

    assert payload["price"] == 250.50
    assert payload["side"] == "SELL"


@pytest.mark.parametrize(
    "side",
    ["BUY", "SELL"],
)
def test_side_is_preserved(side):
    mapper = OrderMapper()

    payload = mapper.to_broker_order(
        symbol="ABC",
        side=side,
        quantity=10,
        order_type="MARKET",
    )

    assert payload["side"] == side


@pytest.mark.parametrize(
    "qty",
    [1, 10, 25, 50, 100],
)
def test_quantity_is_preserved(qty):
    mapper = OrderMapper()

    payload = mapper.to_broker_order(
        symbol="ABC",
        side="BUY",
        quantity=qty,
        order_type="MARKET",
    )

    assert payload["quantity"] == qty
