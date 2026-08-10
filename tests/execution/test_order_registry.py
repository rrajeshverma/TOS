import pytest

from execution.order_registry import OrderRegistry


def test_register_order():
    registry = OrderRegistry()

    order = object()

    registry.register("REQ-1", order)

    assert registry.exists("REQ-1")
    assert registry.get("REQ-1") is order


def test_duplicate_registration():
    registry = OrderRegistry()

    registry.register("REQ-1", object())

    with pytest.raises(ValueError):
        registry.register("REQ-1", object())


def test_remove_order():
    registry = OrderRegistry()

    registry.register("REQ-1", object())

    registry.remove("REQ-1")

    assert not registry.exists("REQ-1")


def test_clear_registry():
    registry = OrderRegistry()

    registry.register("1", object())
    registry.register("2", object())

    registry.clear()

    assert registry.size() == 0


def test_unknown_order_returns_none():
    registry = OrderRegistry()

    assert registry.get("UNKNOWN") is None
