from decimal import Decimal

from domain.instrument import Instrument


def test_create_instrument():
    instrument = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="NSE_FNO",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    assert instrument.symbol == "NIFTY"
    assert instrument.security_id == "13"
    assert instrument.exchange_segment == "NSE_FNO"
    assert instrument.lot_size == 65
    assert instrument.tick_size == Decimal("0.05")


def test_instrument_is_immutable():
    instrument = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="NSE_FNO",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    try:
        instrument.symbol = "BANKNIFTY"
        assert False
    except AttributeError:
        assert True
