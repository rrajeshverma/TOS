from approval.order_validator import OrderValidator
from approval.trade_request import TradeRequest


def create_request():
    return TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )


def test_validator_can_be_created():
    validator = OrderValidator()

    assert validator is not None


def test_valid_order_is_accepted():
    validator = OrderValidator()

    result = validator.validate(create_request())

    assert result["valid"] is True


def test_invalid_side_is_rejected():
    validator = OrderValidator()

    request = TradeRequest(
        symbol="NIFTY",
        side="HOLD",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    result = validator.validate(request)

    assert result["valid"] is False


def test_zero_quantity_is_rejected():
    validator = OrderValidator()

    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=0,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    result = validator.validate(request)

    assert result["valid"] is False


def test_negative_price_is_rejected():
    validator = OrderValidator()

    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=-1,
        strategy="NIFTY_ORB",
        metadata={},
    )

    result = validator.validate(request)

    assert result["valid"] is False


def test_missing_strategy_is_rejected():
    validator = OrderValidator()

    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="",
        metadata={},
    )

    result = validator.validate(request)

    assert result["valid"] is False
