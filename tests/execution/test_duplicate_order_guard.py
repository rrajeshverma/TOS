from execution.duplicate_order_guard import DuplicateOrderGuard
from execution.order_registry import OrderRegistry


def test_should_submit_new_request():
    guard = DuplicateOrderGuard(OrderRegistry())

    assert guard.should_submit("REQ-1")


def test_should_not_submit_duplicate_request():
    registry = OrderRegistry()
    guard = DuplicateOrderGuard(registry)

    guard.register("REQ-1", object())

    assert not guard.should_submit("REQ-1")
