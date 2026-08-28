"""
Tests for completed trade journal flow.
"""

from datetime import date, datetime
from decimal import Decimal

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.risk import Risk
from domain.trade import Trade
from journal.trade_journal import TradeJournal
from shared.enums import (
    DecisionStatus,
    ExitReason,
    Signal,
    TradeStatus,
)
from utils.id_generator import generate_decision_id, generate_trade_id


def create_closed_trade():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=100,
        high=120,
        low=95,
        close=115,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=100,
        ema_low=90,
        vwap=100,
        rsi=60,
    )

    decision = Decision(
        decision_id=generate_decision_id(),
        timestamp=datetime.now(),
        market=market,
        indicator_set=indicators,
        signal=Signal.BUY_CE,
        status=DecisionStatus.VALID,
        reasons=("test",),
    )

    risk = Risk(
        decision=decision,
        approved=True,
        reasons=(),
    )

    return Trade(
        trade_id=generate_trade_id(),
        risk=risk,
        entry_price=Decimal(100),
        stop_loss=Decimal(90),
        target=Decimal(120),
        quantity=65,
        entry_time=datetime.now(),
        exit_price=Decimal(121),
        exit_time=datetime.now(),
        exit_reason=ExitReason.TARGET,
        status=TradeStatus.CLOSED,
        pnl=Decimal(1365),
    )


def test_trade_journal_records_completed_trade(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    trade = create_closed_trade()

    journal.record(trade)

    assert journal.exists()
    assert journal.count() == 1


def test_trade_journal_records_multiple_trades(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    journal.record(create_closed_trade())
    journal.record(create_closed_trade())

    assert journal.count() == 2


def test_trade_journal_file_contains_trade_data(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    trade = create_closed_trade()

    journal.record(trade)

    content = journal_file.read_text()

    assert trade.trade_id in content
    assert "121" in content
    assert "1365" in content


def test_trade_journal_creates_header(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    assert journal.exists()

    content = journal_file.read_text()

    assert "Trade ID" in content
    assert "PnL" in content
    assert "Status" in content


def test_count_today_counts_only_closed_trades(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    today = date(2026, 8, 12)

    trade = create_closed_trade()
    trade = Trade(
        trade_id=trade.trade_id,
        risk=trade.risk,
        entry_price=trade.entry_price,
        stop_loss=trade.stop_loss,
        target=trade.target,
        quantity=trade.quantity,
        entry_time=datetime(2026, 8, 12, 9, 20),
        exit_price=trade.exit_price,
        exit_time=datetime(2026, 8, 12, 9, 25),
        exit_reason=trade.exit_reason,
        status=trade.status,
        pnl=trade.pnl,
    )

    journal.record(trade)

    assert journal.count_today(today) == 1


def test_count_today_excludes_other_dates(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    trade = create_closed_trade()
    trade = Trade(
        trade_id=trade.trade_id,
        risk=trade.risk,
        entry_price=trade.entry_price,
        stop_loss=trade.stop_loss,
        target=trade.target,
        quantity=trade.quantity,
        entry_time=datetime(2026, 8, 11, 9, 20),
        exit_price=trade.exit_price,
        exit_time=datetime(2026, 8, 11, 9, 25),
        exit_reason=trade.exit_reason,
        status=trade.status,
        pnl=trade.pnl,
    )

    journal.record(trade)

    assert journal.count_today(date(2026, 8, 12)) == 0


def test_daily_pnl_returns_realized_pnl(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    trade = create_closed_trade()

    trade = Trade(
        trade_id=trade.trade_id,
        risk=trade.risk,
        entry_price=trade.entry_price,
        stop_loss=trade.stop_loss,
        target=trade.target,
        quantity=trade.quantity,
        entry_time=datetime(2026, 8, 12, 9, 20),
        exit_price=trade.exit_price,
        exit_time=datetime(2026, 8, 12, 9, 25),
        exit_reason=trade.exit_reason,
        status=trade.status,
        pnl=Decimal("1365"),
    )

    journal.record(trade)

    assert journal.daily_pnl(date(2026, 8, 12)) == Decimal("1365")


def test_daily_pnl_returns_zero_when_no_trades(tmp_path):
    journal_file = tmp_path / "trade_journal.csv"

    journal = TradeJournal(
        file_path=str(journal_file),
    )

    assert journal.daily_pnl(date(2026, 8, 12)) == Decimal("0")
