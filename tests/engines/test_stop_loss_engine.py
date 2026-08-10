from decimal import Decimal

import pytest

from engines.stop_loss_engine import StopLossEngine
from shared.enums import Signal


def test_buy_ce_uses_previous_low():
    stop = StopLossEngine().calculate(
        signal=Signal.BUY_CE,
        previous_high=Decimal(25210),
        previous_low=Decimal(25170),
        ema_high=Decimal(25190),
        ema_low=Decimal(25160),
    )

    assert stop.price == Decimal(25170)
    assert stop.reason == "Previous Candle Low"


def test_buy_pe_uses_previous_high():
    stop = StopLossEngine().calculate(
        signal=Signal.BUY_PE,
        previous_high=Decimal(25210),
        previous_low=Decimal(25170),
        ema_high=Decimal(25190),
        ema_low=Decimal(25160),
    )

    assert stop.price == Decimal(25210)
    assert stop.reason == "Previous Candle High"


def test_none_signal_raises_error():
    with pytest.raises(ValueError):
        StopLossEngine().calculate(
            signal=Signal.NONE,
            previous_high=Decimal(25210),
            previous_low=Decimal(25170),
            ema_high=Decimal(25190),
            ema_low=Decimal(25160),
        )
