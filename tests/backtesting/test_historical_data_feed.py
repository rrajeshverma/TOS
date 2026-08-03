from pathlib import Path

from backtesting.csv_data_source import CSVDataSource
from backtesting.historical_data_feed import HistoricalDataFeed


def test_historical_data_feed_from_csv(tmp_path: Path):
    csv_file = tmp_path / "btc.csv"

    csv_file.write_text(
        (
            "timestamp,open,high,low,close,volume\n"
            "2026-01-01T00:00:00,100,105,99,104,1000\n"
            "2026-01-01T00:30:00,104,106,103,105,1200\n"
        ),
        encoding="utf-8",
    )

    source = CSVDataSource(
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="30m",
    )

    markets = source.load(csv_file)

    feed = HistoricalDataFeed(markets)

    first = next(feed)
    second = next(feed)

    assert first.symbol == "BTCUSDT"
    assert first.close == 104.0

    assert second.close == 105.0
