from datetime import datetime
from decimal import Decimal

from domain.instrument import Instrument
from services.nifty_option_selector import NiftyOptionSelector
from shared.enums import Signal
from storage.instrument_repository import InstrumentRepository


def make_option(
    symbol: str,
    security_id: str,
    strike: str,
    option_type: str,
) -> Instrument:
    return Instrument(
        symbol=symbol,
        security_id=security_id,
        exchange_segment="NSE_FNO",
        lot_size=65,
        tick_size=Decimal("0.05"),
        instrument_type="OPTIDX",
        expiry=datetime(2026, 9, 8, 14, 30),
        strike=Decimal(strike),
        option_type=option_type,
    )


def make_repository() -> InstrumentRepository:
    repository = InstrumentRepository()

    for instrument in (
        make_option(
            "NIFTY-Sep2026-23900-CE",
            "10001",
            "23900",
            "CE",
        ),
        make_option(
            "NIFTY-Sep2026-23950-CE",
            "10002",
            "23950",
            "CE",
        ),
        make_option(
            "NIFTY-Sep2026-24000-CE",
            "10003",
            "24000",
            "CE",
        ),
        make_option(
            "NIFTY-Sep2026-24000-PE",
            "10004",
            "24000",
            "PE",
        ),
        make_option(
            "NIFTY-Sep2026-24050-PE",
            "10005",
            "24050",
            "PE",
        ),
        make_option(
            "NIFTY-Sep2026-24100-PE",
            "10006",
            "24100",
            "PE",
        ),
    ):
        repository.add(instrument)

    return repository


def test_buy_ce_selects_one_strike_itm():
    selector = NiftyOptionSelector(make_repository())

    instrument = selector.select(
        underlying_price=Decimal("24080"),
        signal=Signal.BUY_CE,
        as_of=datetime(2026, 9, 2, 10, 0),
    )

    assert instrument.symbol == "NIFTY-Sep2026-24000-CE"
    assert instrument.security_id == "10003"
    assert instrument.strike == Decimal("24000")
    assert instrument.lot_size == 65


def test_buy_pe_selects_one_strike_itm():
    selector = NiftyOptionSelector(make_repository())

    instrument = selector.select(
        underlying_price=Decimal("24020"),
        signal=Signal.BUY_PE,
        as_of=datetime(2026, 9, 2, 10, 0),
    )

    assert instrument.symbol == "NIFTY-Sep2026-24050-PE"
    assert instrument.security_id == "10005"
    assert instrument.strike == Decimal("24050")
    assert instrument.lot_size == 65


def test_expired_contract_is_not_selected():
    repository = InstrumentRepository()

    repository.add(
        Instrument(
            symbol="NIFTY-Old-24000-CE",
            security_id="99999",
            exchange_segment="NSE_FNO",
            lot_size=65,
            tick_size=Decimal("0.05"),
            instrument_type="OPTIDX",
            expiry=datetime(2026, 9, 1, 14, 30),
            strike=Decimal("24000"),
            option_type="CE",
        )
    )

    selector = NiftyOptionSelector(repository)

    try:
        selector.select(
            underlying_price=Decimal("24080"),
            signal=Signal.BUY_CE,
            as_of=datetime(2026, 9, 2, 10, 0),
        )
        assert False, "Expected LookupError"
    except LookupError:
        pass
