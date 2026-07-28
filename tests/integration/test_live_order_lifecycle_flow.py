"""
Tests:
Live Order Lifecycle Flow

Flow:

Execution
   |
   ▼
Order Registration
   |
   ▼
Order Tracking
"""

from execution.order_registry import OrderRegistry


class DummyOrder:
    def __init__(
        self,
        status="SUBMITTED",
    ):
        self.status = status


def test_order_can_be_registered():

    registry = OrderRegistry()

    order = DummyOrder()

    registry.register(
        "ORDER001",
        order,
    )

    assert registry.exists(
        "ORDER001"
    )


def test_registered_order_can_be_retrieved():

    registry = OrderRegistry()

    order = DummyOrder()

    registry.register(
        "ORDER001",
        order,
    )

    stored = registry.get(
        "ORDER001"
    )

    assert stored == order


def test_duplicate_order_is_rejected():

    registry = OrderRegistry()

    order = DummyOrder()

    registry.register(
        "ORDER001",
        order,
    )

    try:
        registry.register(
            "ORDER001",
            order,
        )

    except ValueError:
        assert True

    else:
        assert False


def test_order_can_be_removed():

    registry = OrderRegistry()

    registry.register(
        "ORDER001",
        DummyOrder(),
    )

    registry.remove(
        "ORDER001"
    )

    assert not registry.exists(
        "ORDER001"
    )


def test_registry_clear():

    registry = OrderRegistry()

    registry.register(
        "ORDER001",
        DummyOrder(),
    )

    registry.clear()

    assert registry.size() == 0