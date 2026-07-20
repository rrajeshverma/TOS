from decimal import Decimal

from domain.instrument import Instrument
from loaders.instrument_csv_loader import InstrumentCSVLoader


def test_load_instruments():
    loader = InstrumentCSVLoader()

    instruments = loader.load("tests/data/instruments.csv")

    assert len(instruments) == 2

    assert instruments[0] == Instrument(
        symbol="NIFTY",
        security_id="13",
        exchange_segment="NSE_FNO",
        lot_size=65,
        tick_size=Decimal("0.05"),
    )

    assert instruments[1] == Instrument(
        symbol="BANKNIFTY",
        security_id="25",
        exchange_segment="NSE_FNO",
        lot_size=35,
        tick_size=Decimal("0.05"),
    )


def test_empty_csv_returns_empty_list(tmp_path):
    csv_file = tmp_path / "empty.csv"

    csv_file.write_text("symbol,security_id,exchange_segment,lot_size,tick_size\n")

    loader = InstrumentCSVLoader()

    instruments = loader.load(csv_file)

    assert instruments == []


def test_skip_invalid_rows(tmp_path):
    csv_file = tmp_path / "invalid.csv"

    csv_file.write_text(
        "symbol,security_id,exchange_segment,lot_size,tick_size\n"
        "NIFTY,13,NSE_FNO,65,0.05\n"
        "BADROW\n"
        "BANKNIFTY,25,NSE_FNO,35,0.05\n"
    )

    loader = InstrumentCSVLoader()

    instruments = loader.load(csv_file)

    assert len(instruments) == 2
