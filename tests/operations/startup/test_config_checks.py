from operations.startup.checks import (
    api_key_check,
    broker_name_check,
    trading_mode_check,
)


def test_valid_api_key():
    assert api_key_check("abc123xyz")


def test_empty_api_key():
    assert not api_key_check("")


def test_blank_api_key():
    assert not api_key_check("   ")


def test_none_api_key():
    assert not api_key_check(None)


def test_long_api_key():
    assert api_key_check("x" * 128)


def test_valid_broker():
    assert broker_name_check("DHAN")


def test_valid_delta():
    assert broker_name_check("DELTA")


def test_lowercase_broker():
    assert broker_name_check("dhan")


def test_invalid_broker():
    assert not broker_name_check("ZERODHA")


def test_empty_broker():
    assert not broker_name_check("")


def test_live_mode():
    assert trading_mode_check("LIVE")


def test_paper_mode():
    assert trading_mode_check("PAPER")


def test_backtest_mode():
    assert trading_mode_check("BACKTEST")


def test_lowercase_mode():
    assert trading_mode_check("paper")


def test_invalid_mode():
    assert not trading_mode_check("TEST")


def test_none_mode():
    assert not trading_mode_check(None)


def test_api_returns_bool():
    assert isinstance(api_key_check("abc"), bool)


def test_broker_returns_bool():
    assert isinstance(broker_name_check("DHAN"), bool)


def test_mode_returns_bool():
    assert isinstance(trading_mode_check("LIVE"), bool)


def test_spaces_trimmed():
    assert broker_name_check(" DHAN ")
