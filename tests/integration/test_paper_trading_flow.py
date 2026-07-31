from services.order_execution_adapter import OrderExecutionAdapter


class FakePaperBroker:
    def __init__(self):
        self.orders = []

    def place_order(self, order):
        self.orders.append(order)

        return {
            "orderId": "PAPER001",
            "status": "SUBMITTED",
        }


def test_execution_engine_with_broker():
    broker = FakePaperBroker()

    adapter = OrderExecutionAdapter(broker=broker)

    result = adapter.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
            "price": 25000,
        }
    )

    assert result["orderId"] == "PAPER001"


def test_broker_receives_order():
    broker = FakePaperBroker()

    adapter = OrderExecutionAdapter(broker=broker)

    adapter.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
            "price": 25000,
        }
    )

    assert len(broker.orders) == 1


def test_buy_order_payload():
    broker = FakePaperBroker()

    adapter = OrderExecutionAdapter(broker=broker)

    order = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
        "price": 25000,
    }

    adapter.execute(order)

    assert broker.orders[0]["side"] == "BUY"


def test_sell_order_payload():
    broker = FakePaperBroker()

    adapter = OrderExecutionAdapter(broker=broker)

    adapter.execute(
        {
            "symbol": "NIFTY",
            "side": "SELL",
            "quantity": 65,
            "price": 25000,
        }
    )

    assert broker.orders[0]["side"] == "SELL"


def test_quantity_preserved():
    broker = FakePaperBroker()

    adapter = OrderExecutionAdapter(broker=broker)

    adapter.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
            "price": 25000,
        }
    )

    assert broker.orders[0]["quantity"] == 65
