import math

from analytics.recovery_ratio import RecoveryRatio


def test_zero_profit():
    ratio = RecoveryRatio()

    assert (
        ratio.calculate(
            net_profit=0,
            max_drawdown=100,
        )
        == 0.0
    )


def test_zero_drawdown():
    ratio = RecoveryRatio()

    assert (
        ratio.calculate(
            net_profit=100,
            max_drawdown=0,
        )
        == 0.0
    )


def test_equal_values():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=100,
        max_drawdown=100,
    )

    assert math.isclose(result, 1.0)


def test_double_ratio():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=200,
        max_drawdown=100,
    )

    assert math.isclose(result, 2.0)


def test_half_ratio():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=100,
        max_drawdown=200,
    )

    assert math.isclose(result, 0.5)


def test_negative_profit():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=-100,
        max_drawdown=50,
    )

    assert math.isclose(result, -2.0)


def test_negative_drawdown():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=150,
        max_drawdown=-75,
    )

    assert math.isclose(result, 2.0)


def test_decimal_values():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=123.45,
        max_drawdown=61.725,
    )

    assert math.isclose(result, 2.0)


def test_result_is_float():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=100,
        max_drawdown=25,
    )

    assert isinstance(result, float)


def test_precision():
    ratio = RecoveryRatio()

    result = ratio.calculate(
        net_profit=99.999,
        max_drawdown=33.333,
    )

    assert math.isclose(
        result,
        3.0,
        rel_tol=1e-9,
    )
