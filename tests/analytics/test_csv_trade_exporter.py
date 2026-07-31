import csv

from analytics.csv_trade_exporter import CSVTradeExporter


def test_export_empty(tmp_path):
    filename = tmp_path / "trades.csv"

    exporter = CSVTradeExporter()

    exporter.export([], filename)

    with open(filename) as file:
        rows = list(csv.reader(file))

    assert rows == [["symbol", "entry", "exit", "qty", "pnl"]]


def test_export_trades(tmp_path):
    filename = tmp_path / "trades.csv"

    trades = [
        {
            "symbol": "NIFTY",
            "entry": 25000,
            "exit": 25100,
            "qty": 50,
            "pnl": 100,
        }
    ]

    exporter = CSVTradeExporter()

    exporter.export(trades, filename)

    with open(filename) as file:
        rows = list(csv.reader(file))

    assert rows[1] == [
        "NIFTY",
        "25000",
        "25100",
        "50",
        "100",
    ]
