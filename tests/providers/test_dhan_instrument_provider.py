from decimal import Decimal

from providers.dhan_instrument_provider import DhanInstrumentProvider


def test_load_nifty_index():
    provider = DhanInstrumentProvider()

    instruments = list(provider.load())

    nifty = next(
        instrument
        for instrument in instruments
        if instrument.security_id == "13" and instrument.exchange_segment == "IDX_I"
    )

    assert nifty.symbol == "NIFTY"
    assert nifty.security_id == "13"
    assert nifty.exchange_segment == "IDX_I"
    assert nifty.lot_size == 1
    assert nifty.tick_size == Decimal("0.0500")
