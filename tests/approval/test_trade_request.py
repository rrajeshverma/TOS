from approval.trade_request import TradeRequest


def test_trade_request_can_be_created():
    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    assert request is not None


def test_trade_request_stores_symbol():
    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    assert request.symbol == "NIFTY"


def test_trade_request_stores_side():
    request = TradeRequest(
        symbol="NIFTY",
        side="SELL",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    assert request.side == "SELL"


def test_trade_request_stores_quantity():
    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    assert request.quantity == 65


def test_trade_request_has_metadata():
    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={
            "source": "strategy",
        },
    )

    assert isinstance(
        request.metadata,
        dict,
    )


def test_trade_request_is_immutable():
    request = TradeRequest(
        symbol="NIFTY",
        side="BUY",
        quantity=65,
        price=20000,
        strategy="NIFTY_ORB",
        metadata={},
    )

    try:
        request.side = "SELL"
        assert False

    except Exception:
        assert True
