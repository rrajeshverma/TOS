from __future__ import annotations

from datetime import datetime
from pathlib import Path

from domain.trade_journal_entry import TradeJournalEntry
from services.trade_journal import TradeJournal


def create_entry(
    symbol: str = "NIFTY",
    side: str = "BUY",
    quantity: int = 50,
    entry_price: float = 100.0,
    exit_price: float = 105.0,
    pnl: float = 250.0,
    strategy: str = "ORB",
    status: str = "CLOSED",
) -> TradeJournalEntry:
    return TradeJournalEntry(
        timestamp=datetime(2026, 8, 1, 9, 30),
        symbol=symbol,
        side=side,
        quantity=quantity,
        entry_price=entry_price,
        exit_price=exit_price,
        pnl=pnl,
        strategy=strategy,
        status=status,
    )


def test_creates_csv_file(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    TradeJournal(str(filename))

    assert filename.exists()


def test_writes_header(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    TradeJournal(str(filename))

    lines = filename.read_text().splitlines()

    assert lines[0] == (
        "timestamp,symbol,side,quantity,entry_price,exit_price,pnl,strategy,status"
    )


def test_records_single_trade(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))
    journal.record(create_entry())

    lines = filename.read_text().splitlines()

    assert len(lines) == 2


def test_records_multiple_trades(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry())
    journal.record(create_entry(symbol="BANKNIFTY"))

    lines = filename.read_text().splitlines()

    assert len(lines) == 3


def test_header_written_only_once(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry())
    journal.record(create_entry())

    lines = filename.read_text().splitlines()

    header_count = sum(1 for line in lines if line.startswith("timestamp"))

    assert header_count == 1


def test_records_symbol(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry(symbol="BANKNIFTY"))

    text = filename.read_text()

    assert "BANKNIFTY" in text


def test_records_buy_side(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry(side="BUY"))

    text = filename.read_text()

    assert "BUY" in text


def test_records_sell_side(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry(side="SELL"))

    text = filename.read_text()

    assert "SELL" in text


def test_records_pnl(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry(pnl=525.75))

    text = filename.read_text()

    assert "525.75" in text


def test_records_strategy(tmp_path: Path):
    filename = tmp_path / "journal.csv"

    journal = TradeJournal(str(filename))

    journal.record(create_entry(strategy="CPR"))

    text = filename.read_text()

    assert "CPR" in text
