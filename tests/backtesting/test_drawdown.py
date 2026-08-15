from decimal import Decimal

from backtesting.drawdown import Drawdown


def test_maximum_drawdown():
    drawdown = Drawdown(
        [
            Decimal("100"),
            Decimal("150"),
            Decimal("70"),
            Decimal("-30"),
            Decimal("10"),
        ]
    )

    assert drawdown.maximum == Decimal("180")


def test_empty_equity_has_zero_drawdown():
    drawdown = Drawdown([])

    assert drawdown.maximum == Decimal("0")


def test_rising_equity_has_zero_drawdown():
    drawdown = Drawdown(
        [
            Decimal("100"),
            Decimal("150"),
            Decimal("175"),
        ]
    )

    assert drawdown.maximum == Decimal("0")


def test_drawdown_recovers_after_decline():
    drawdown = Drawdown(
        [
            Decimal("100"),
            Decimal("150"),
            Decimal("100"),
            Decimal("125"),
        ]
    )

    assert drawdown.maximum == Decimal("50")
