from pathlib import Path

from backtesting.csv_data_source import CSVDataSource
from domain.market import Market


def test_load_returns_market_objects(tmp_path: Path):
    csv_file = tmp_path / "btc.csv"

    csv_file.write_text(
        ("timestamp,open,high,low,close,volume\n2026-01-01T00:00:00,100,105,99,104,1000\n"),
        encoding="utf-8",
    )

    source = CSVDataSource(
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="30m",
    )

    markets = list(source.load(csv_file))

    assert len(markets) == 1

    market = markets[0]

    assert isinstance(market, Market)
    assert market.symbol == "BTCUSDT"
    assert market.exchange == "BINANCE"
    assert market.timeframe == "30m"
    assert market.close == 104.0
    assert market.volume == 1000
