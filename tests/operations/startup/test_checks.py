from operations.startup.checks import (
    always_pass,
    always_fail,
    capital_check,
    risk_check,
)


def test_always_pass():
    assert always_pass()


def test_always_fail():
    assert not always_fail()


def test_valid_capital():
    assert capital_check(100000)


def test_small_capital():
    assert capital_check(1)


def test_zero_capital():
    assert not capital_check(0)


def test_negative_capital():
    assert not capital_check(-100)


def test_large_capital():
    assert capital_check(10_000_000)


def test_valid_risk():
    assert risk_check(2)


def test_half_percent_risk():
    assert risk_check(0.5)


def test_maximum_risk():
    assert risk_check(100)


def test_zero_risk():
    assert not risk_check(0)


def test_negative_risk():
    assert not risk_check(-5)


def test_over_100_risk():
    assert not risk_check(150)


def test_float_risk():
    assert risk_check(1.25)


def test_integer_risk():
    assert risk_check(5)


def test_capital_returns_bool():
    assert isinstance(capital_check(1000), bool)


def test_risk_returns_bool():
    assert isinstance(risk_check(2), bool)


def test_always_pass_returns_bool():
    assert isinstance(always_pass(), bool)


def test_always_fail_returns_bool():
    assert isinstance(always_fail(), bool)


def test_multiple_calls():
    for _ in range(10):
        assert capital_check(1000)
