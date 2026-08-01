from strategies.filters.vwap_filter import VWAPFilter


def test_buy_allowed():
    assert VWAPFilter().buy_allowed(
        close=105,
        vwap=100,
    )


def test_buy_not_allowed_when_equal():
    assert not VWAPFilter().buy_allowed(
        close=100,
        vwap=100,
    )


def test_buy_not_allowed_when_below():
    assert not VWAPFilter().buy_allowed(
        close=99,
        vwap=100,
    )


def test_sell_allowed():
    assert VWAPFilter().sell_allowed(
        close=95,
        vwap=100,
    )


def test_sell_not_allowed_when_equal():
    assert not VWAPFilter().sell_allowed(
        close=100,
        vwap=100,
    )


def test_sell_not_allowed_when_above():
    assert not VWAPFilter().sell_allowed(
        close=101,
        vwap=100,
    )
