from brokers.core.broker_registry import BrokerRegistry


class DummyBroker:
    pass


def test_register_broker():
    registry = BrokerRegistry()

    broker = DummyBroker()

    registry.register("paper", broker)

    assert registry.get("paper") is broker


def test_unregister_broker():
    registry = BrokerRegistry()

    registry.register("paper", DummyBroker())

    registry.unregister("paper")

    assert registry.get("paper") is None


def test_default_broker():
    registry = BrokerRegistry()

    broker = DummyBroker()

    registry.register("paper", broker)
    registry.set_default("paper")

    assert registry.get_default() is broker


def test_duplicate_registration_updates_broker():
    registry = BrokerRegistry()

    first = DummyBroker()
    second = DummyBroker()

    registry.register("paper", first)
    registry.register("paper", second)

    assert registry.get("paper") is second


def test_registry_summary():
    registry = BrokerRegistry()

    registry.register("paper", DummyBroker())

    summary = registry.summary()

    assert summary["count"] == 1
    assert "paper" in summary["brokers"]