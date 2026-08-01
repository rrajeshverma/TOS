from strategies.filters.ema_filter import EMAFilter


def test_buy_allowed():
    assert EMAFilter().buy_allowed(
        close=105,
        ema_high=100,
    )


def test_buy_not_allowed_when_equal():
    assert not EMAFilter().buy_allowed(
        close=100,
        ema_high=100,
    )


def test_buy_not_allowed_when_below():
    assert not EMAFilter().buy_allowed(
        close=99,
        ema_high=100,
    )


def test_sell_allowed():
    assert EMAFilter().sell_allowed(
        close=95,
        ema_low=100,
    )


def test_sell_not_allowed_when_equal():
    assert not EMAFilter().sell_allowed(
        close=100,
        ema_low=100,
    )


def test_sell_not_allowed_when_above():
    assert not EMAFilter().sell_allowed(
        close=101,
        ema_low=100,
    )
