import tempfile

from market.csv_market_loader import CSVMarketLoader


def test_load_single_tick():
    csv = """symbol,price,volume
NIFTY,25000,100
"""

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(csv)
        filename = f.name

    loader = CSVMarketLoader()

    ticks = loader.load(filename)

    assert len(ticks) == 1
    assert ticks[0]["symbol"] == "NIFTY"
    assert ticks[0]["price"] == 25000.0
    assert ticks[0]["volume"] == 100


def test_load_multiple_ticks():
    csv = """symbol,price,volume
NIFTY,25000,100
NIFTY,25001,120
"""

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(csv)
        filename = f.name

    loader = CSVMarketLoader()

    ticks = loader.load(filename)

    assert len(ticks) == 2
