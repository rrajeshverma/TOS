import pytest

from execution.signal_mapper import SignalMapper
from shared.enums import OrderSide, Signal


def test_buy_ce_maps_to_buy():
    assert (
        SignalMapper.to_order_side(Signal.BUY_CE)
        == OrderSide.BUY
    )


def test_buy_pe_maps_to_buy():
    assert (
        SignalMapper.to_order_side(Signal.BUY_PE)
        == OrderSide.BUY
    )


def test_none_signal_raises_value_error():
    with pytest.raises(ValueError):
        SignalMapper.to_order_side(Signal.NONE)