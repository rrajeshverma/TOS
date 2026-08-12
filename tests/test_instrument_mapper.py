from decimal import Decimal

import pytest

from brokers.instrument_mapper import InstrumentMapper
from domain.instrument import Instrument
from storage.instrument_repository import InstrumentRepository


def test_map_symbol_to_instrument():
    repo = InstrumentRepository()

    instrument = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="NSE_FNO",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    repo.add(instrument)

    mapper = InstrumentMapper(repo)

    assert mapper.get("NIFTY") == instrument


def test_unknown_symbol_raises_keyerror():
    repo = InstrumentRepository()

    mapper = InstrumentMapper(repo)

    with pytest.raises(KeyError):
        mapper.get("INVALID")


def test_map_security_id_to_instrument():
    repo = InstrumentRepository()

    instrument = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="IDX_I",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    repo.add(instrument)

    mapper = InstrumentMapper(repo)

    assert mapper.get_by_security_id("13", "IDX_I") == instrument


def test_unknown_security_id_raises_keyerror():
    repo = InstrumentRepository()

    mapper = InstrumentMapper(repo)

    with pytest.raises(KeyError):
        mapper.get_by_security_id("999", "IDX_I")
