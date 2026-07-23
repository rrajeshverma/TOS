from brokers.core.broker_router import BrokerRouter


class DummyBroker:
    def get_positions(self):
        return ["POSITION"]

    def get_funds(self):
        return {"cash": 100000}

    def place_order(self, order):
        return {"order": order}

    def is_connected(self):
        return True


def test_route_market_data():
    broker = DummyBroker()

    router = BrokerRouter(broker)

    result = router.route_market_data()

    assert result == []


def test_route_orders():
    broker = DummyBroker()

    router = BrokerRouter(broker)

    result = router.route_order("BUY")

    assert result == {"order": "BUY"}


def test_route_positions():
    broker = DummyBroker()

    router = BrokerRouter(broker)

    result = router.route_positions()

    assert result == ["POSITION"]


def test_route_account():
    broker = DummyBroker()

    router = BrokerRouter(broker)

    result = router.route_account()

    assert result == {"cash": 100000}


def test_router_health():
    broker = DummyBroker()

    router = BrokerRouter(broker)

    assert router.health() is True
