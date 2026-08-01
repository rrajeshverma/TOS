from strategies.filters.rsi_filter import RSIFilter


def test_buy_allowed():
    assert RSIFilter().buy_allowed(56)


def test_buy_not_allowed():
    assert not RSIFilter().buy_allowed(55)


def test_sell_allowed():
    assert RSIFilter().sell_allowed(44)


def test_sell_not_allowed():
    assert not RSIFilter().sell_allowed(45)


def test_neutral_lower():
    assert RSIFilter().neutral(45)


def test_neutral_middle():
    assert RSIFilter().neutral(50)


def test_neutral_upper():
    assert RSIFilter().neutral(55)


def test_not_neutral_buy():
    assert not RSIFilter().neutral(60)


def test_not_neutral_sell():
    assert not RSIFilter().neutral(40)
