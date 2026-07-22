from live.order_validator import OrderValidator


def valid_order():

    return {
        "symbol": "NIFTY",
        "quantity": 65,
        "price": 25000,
    }


def test_valid_order():

    validator = OrderValidator()

    assert validator.validate(
        valid_order()
    )


def test_invalid_quantity():

    order = valid_order()
    order["quantity"] = 0

    assert not OrderValidator().validate(order)


def test_invalid_price():

    order = valid_order()
    order["price"] = -1

    assert not OrderValidator().validate(order)


def test_missing_symbol():

    order = valid_order()
    del order["symbol"]

    assert not OrderValidator().validate(order)


def test_validation_result():

    result = OrderValidator().validate(
        valid_order()
    )

    assert result is True