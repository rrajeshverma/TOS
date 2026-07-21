from datetime import datetime
from decimal import Decimal

from domain.market import Market
from domain.indicator_set import IndicatorSet

from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory

from journal.trade_journal import TradeJournal

from shared.enums import TradeStatus


def create_trade():

    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24990,
        high=25010,
        low=24980,
        close=25000,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )

    trade = TradeFactory().create(
        risk=risk,
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24950"),
    )

    # Simulate a completed trade
    object.__setattr__(trade, "status", TradeStatus.CLOSED)
    object.__setattr__(trade, "exit_price", Decimal("25100"))
    object.__setattr__(trade, "exit_time", datetime.now())
    object.__setattr__(trade, "pnl", Decimal("6500"))

    return trade


def test_trade_journal(tmp_path):

    journal = TradeJournal(file_path=str(tmp_path / "trade_journal.csv"))

    trade = create_trade()

    journal.record(trade)

    assert journal.exists()

def test_trade_journal_count_empty(tmp_path):
    journal = TradeJournal(file_path=str(tmp_path / "trade_journal.csv"))

    assert journal.count() == 0


def test_trade_journal_count_after_record(tmp_path):
    journal = TradeJournal(file_path=str(tmp_path / "trade_journal.csv"))

    journal.record(create_trade())

    assert journal.count() == 1


def test_trade_journal_count_multiple_records(tmp_path):
    journal = TradeJournal(file_path=str(tmp_path / "trade_journal.csv"))

    journal.record(create_trade())
    journal.record(create_trade())
    journal.record(create_trade())

    assert journal.count() == 3


def test_trade_journal_count_missing_file(tmp_path):
    journal = TradeJournal(file_path=str(tmp_path / "missing" / "trade_journal.csv"))

    # Simulate the file being removed after initialization.
    journal.file_path.unlink()

    assert journal.count() == 0
