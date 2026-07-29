from execution.order_validator import (
    OrderValidator,
)


class DummyOrder:
    def __init__(
        self,
        symbol="NIFTY",
        quantity=65,
    ):
        self.symbol = symbol
        self.quantity = quantity


def test_valid_order_is_accepted():
    validator = OrderValidator()

    order = DummyOrder()

    assert validator.validate(order) is True


def test_none_order_is_rejected():
    validator = OrderValidator()

    assert validator.validate(None) is False


def test_zero_quantity_is_rejected():
    validator = OrderValidator()

    order = DummyOrder(quantity=0)

    assert validator.validate(order) is False


def test_negative_quantity_is_rejected():
    validator = OrderValidator()

    order = DummyOrder(quantity=-65)

    assert validator.validate(order) is False


def test_missing_symbol_is_rejected():
    validator = OrderValidator()

    class InvalidOrder:
        quantity = 65

    assert validator.validate(InvalidOrder()) is False


def test_missing_quantity_is_rejected():
    validator = OrderValidator()

    class InvalidOrder:
        symbol = "NIFTY"

    assert validator.validate(InvalidOrder()) is False
