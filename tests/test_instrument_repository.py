from decimal import Decimal

from domain.instrument import Instrument
from storage.instrument_repository import InstrumentRepository


def test_add_and_get_by_symbol():
    repo = InstrumentRepository()

    instrument = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="IDX_I",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    repo.add(instrument)

    assert repo.get_by_symbol("NIFTY") == instrument


def test_get_by_security_id():
    repo = InstrumentRepository()

    instrument = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="IDX_I",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    repo.add(instrument)

    assert repo.get_by_security_id("13", "IDX_I") == instrument


def test_list_all():
    repo = InstrumentRepository()

    repo.add(
        Instrument(
            "NIFTY",
            "13",
            "NSE_FNO",
            65,
            Decimal("0.05"),
        )
    )

    repo.add(
        Instrument(
            "BANKNIFTY",
            "25",
            "NSE_FNO",
            35,
            Decimal("0.05"),
        )
    )

    assert len(repo.list_all()) == 2


def test_unknown_symbol_raises_keyerror():
    repo = InstrumentRepository()

    try:
        repo.get_by_symbol("INVALID")
        assert False
    except KeyError:
        assert True


def test_unknown_security_id_raises_keyerror():
    repo = InstrumentRepository()

    try:
        repo.get_by_security_id("999", "IDX_I")
        assert False
    except KeyError:
        assert True


def test_same_security_id_can_exist_across_exchange_segments():
    repo = InstrumentRepository()

    abb = Instrument(
        symbol="ABB",
        security_id="13",
        exchange_segment="NSE_EQ",
        lot_size=1,
        tick_size=Decimal("0.05"),
    )

    nifty = Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="IDX_I",
        lot_size=1,
        tick_size=Decimal("0.05"),
    )

    repo.add(abb)
    repo.add(nifty)

    assert repo.get_by_security_id("13", "NSE_EQ") == abb
    assert repo.get_by_security_id("13", "IDX_I") == nifty
